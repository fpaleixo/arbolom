%Generates the best candidate function for stable state observations.
%(In stable state mode we must ensure that, given the values of a compound's
%regulators, the compound is able to replicate its observed state).

#const compound = c.
#const hard_limit = 10.

%*--Identifying inconsistency type--*%
%If the compound is inconsistent because it outputs 1 when 0 was expected, 
%we have a positive inconsistency
positive_inconsistencies :- inconsistent(_,compound,1).

%If the compound is inconsistent because it outputs 0 when 1 was expected, 
%we have a negative inconsistency
negative_inconsistencies :- inconsistent(_,compound,0).

%If we have positive inconsistencies but no negative inconsistencies, we need
%to obtain a more restrictive function
restrain_function :- positive_inconsistencies, not negative_inconsistencies.

%If we have negative inconsistencies but no positive inconsistencies, we need
%to obtain a more general function
generalize_function :- negative_inconsistencies, not positive_inconsistencies.

%Define
%*--Fixed regulators--*%
%fixed/2 tells us that regulator C has to be one of the compound's regulators
fixed_regulator(C) :- fixed(C,compound), compound(C).
fixed_regulator(C) :- fixed(C,compound,_), compound(C).

%Fixed/3. contains information regarding the sign of a fixed regulator
fixed_activator(C) :- fixed(C,compound,0), compound(C).
fixed_inhibitor(C) :- fixed(C,compound,1), compound(C).

%*--Assigning regulator signs--*%
%Fixed activators and inhibitors already have their regulation behavior defined
activator(C) :- fixed_activator(C).
inhibitor(C) :- fixed_inhibitor(C).

%A compound C can either be an inhibitor or an activator, but not both
1 {activator(C); inhibitor(C)} 1 :- compound(C), 
  not fixed_activator(C), not fixed_inhibitor(C).

%Keep track of which original regulators C had their sign changed
%(used in minimization #3)
sign_changed(C) :- regulates(C,compound,0), inhibitor(C).
sign_changed(C) :- regulates(C,compound,1), activator(C).

%*--Creating nodes--*%
%If we have at least some observation where the compound is active,
%then we have positive observations
positive_observations :- curated_observation(_,compound,1).

%If the function needs to be more restrictive, we should be able to find
%a solution using a lesser or equal number of nodes than it already has 
maximum_node_number(TN) :- positive_observations,
  restrain_function, function(compound,TN).

%If the function does not need to be more restrictive, then we should be able
%to find a solution using the minimum between the number of positive
%observations that were violated plus the number of already existing nodes,
%and 10, which is the value after which the functions in a very heavy example
%(40 variables, 5 experiments, 20 time steps, 31 inconsistent functions),
%take longer than 1 second to solve (also, 10 is double the amount of the number
%of nodes present in the largest real-world function we work with)
maximum_node_number(MIN) :- positive_observations,
  not restrain_function, function(compound,TN),
  PR = #count{E : curated_observation(E,compound,1), 
  inconsistent(E,compound,0)},
  MIN = #min{hard_limit; PR + TN}.

%If we have no positive observations, then we will use 1 node maximum to explain the observations.
%If 1 node isn't enough to produce a function that's restrictive enough, then no such function exists
%(since considering more nodes would never allow us to create more restrictive fuctions, only more general ones)
maximum_node_number(1) :- not positive_observations.

%Distribute compounds across nodes
1 {node_regulator(1..MN,C) : maximum_node_number(MN), compound(C)}.

%Project node IDs into their own predicate
node_ID(N) :- node_regulator(N,_).

%*--Choosing the candidate nodes--*%
%If one of a node's variables has value 0 for experiment E, 
%then for that same experiment the node will also have value 0 (if that variable is an activator)
experiment_negative_node(E,N) :- node_regulator(N,C), curated_observation(E,C,0), activator(C).
%Variant for variables that are inhibitors
experiment_negative_node(E,N) :- node_regulator(N,C), curated_observation(E,C,1), inhibitor(C).

%Nodes that aren't negative in experiment E must be positive
experiment_positive_node(E,N) :- not experiment_negative_node(E,N), node_ID(N), curated_observation(E,_,_).

%Determine all positive observations that are covered by the selected nodes (i.e. positive observations that can
%be obtained by those nodes, since the nodes are positive in the experiment they occur)
node_positive_observation_coverage(N,E) :- curated_observation(E,compound,1), 
  experiment_positive_node(E,N).

%If two candidate nodes cover different positive observations, then their behavior is distinct
%(used in integrity constraint #3)
nodes_distinct_coverage(N1,N2) :- node_ID(N1), node_ID(N2), N1 < N2, 
  node_positive_observation_coverage(N1,E), 
  not node_positive_observation_coverage(N2,E).

%*--Identifying missing/extra regulators--*%
%An original_regulator C is a regulator that is present in the original inconsistent function
original_regulator(C) :- regulates(C,compound,_).

%If a regulator C is present in node N, then we define it as a present_regulator
present_regulator(C) :- node_regulator(N,C).

%If an original regulator C is not present in any node, we define it as a missing_regulator
missing_regulator(C) :- original_regulator(C), not present_regulator(C).

%If a present regulator C is not one of the original regulators, we define it as an extra_regulator
extra_regulator(C) :- not original_regulator(C), present_regulator(C).
 
%*--Verifying whether the rule that no node can contain another node has been broken (BCF)--*%
%Calculate the number of regulators per candidate node
node_regulator_number(N,N_VARNO) :- N_VARNO = #count{ C : node_regulator(N,C) }, node_ID(N).

%If the number of variables in one node is equal to the number of variables that it has in common with another node,
%then the first node is fully contained within the second node, and so the BCF has been broken
bcf_broken :- node_ID(N1), node_ID(N2), N1 != N2, node_regulator_number(N1,N1_VARNO),
  COMMON_VARNO = #count{C : node_regulator(N1,C), node_regulator(N2,C)}, COMMON_VARNO = N1_VARNO.


%Test
%1-We're only interested in generating nodes that can be used to explain the observations,
%which is not possible for a node to do if it is active when we expect it to be inactive
:- experiment_positive_node(E,N), curated_observation(E,compound,0).

%2-Every positive observation must be covered by some positive node
:- curated_observation(E,compound,1), not node_positive_observation_coverage(_,E).

%3-If two candidate nodes share the same behavior, then the solution is not optimal
:- node_ID(N1), node_ID(N2), N1 < N2, not nodes_distinct_coverage(N1,N2).

%4-The BCF cannot be broken (nodes cannot contain other nodes)
:- bcf_broken.

%5-Fixed regulators must be present in the final solution
:- fixed_regulator(C), not node_regulator(_,C).


%Display
regulator_activator(C) :- node_regulator(N,C), activator(C).
regulator_inhibitor(C) :- node_regulator(N,C), inhibitor(C).

#show node_ID/1.
#show regulator_activator/1.
#show regulator_inhibitor/1.
#show node_regulator/2.

%Optimize
%1-Optimize for the minimum number of final nodes (highest priority)
#minimize{1@3,N : node_ID(N)}.

%2-Optimize for the minimum changes to regulators
#minimize{1@2,C : missing_regulator(C)}.
#minimize{1@2,C : extra_regulator(C)}.

%3-Optimize for the minimum changes to regulator signs (lowest priority)
#minimize{1@1,C : sign_changed(C)}.
