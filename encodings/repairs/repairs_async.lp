%Generates the best candidate function for asynchronous observations
#const compound = c.

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
%If we have at least some observation where the compound is active at a T > 0,
%then we have positive observations
positive_observations :- curated_observation(E,T,compound,1), 
  curated_observation(E,T-1,compound,0), T > 0.

%The highest number of nodes we'll consider is equal to the number of unique positive observations,
%since at most we'll need one node per unique positive observation to render the model consistent
%(we may use less, since it can happen that one node is able explain several positive observations)
maximum_node_number(POSITIVE_OBSERVATIONS_COUNT) :- positive_observations,
  POSITIVE_OBSERVATIONS_COUNT = #count{E,T,compound,1 : unique_positive_observation(E,T)}.

%If we have no positive observations, then we will use 1 node maximum to explain the observations.
%If 1 node isn't enough to produce a function that's restrictive enough, then no such function exists
%(since considering more nodes would never allow us to create more restrictive fuctions, only more general ones)
maximum_node_number(1) :- not positive_observations.

%If a compound C is active in the time step before a positive observation, then it is a potential regulator
%that could be used to explain that observation
observation_potential_regulator(E,T,C) :- curated_observation(E,T-1,C,1), activator(C), unique_positive_observation(E,T).
%Variant for inhibitors
observation_potential_regulator(E,T,C) :- curated_observation(E,T-1,C,0), inhibitor(C), unique_positive_observation(E,T).

%Distribute potential regulators C for a given observation E,T across nodes
1 {node_regulator(1..MN,C) : maximum_node_number(MN), observation_potential_regulator(E,T,C)} :- unique_positive_observation(E,T).

%If we have no positive observations, we only need to assign regulators to a single node
1 {node_regulator(1,C) : compound(C)} :- not positive_observations.

%Project node IDs into their own predicate
node_ID(N) :- node_regulator(N,_).

%*--Choosing the candidate nodes--*%
%If one of a node N's regulators has value 0 for experiment E at time step T, 
%then for that same experiment and time step the node will also have value 0 (if that variable is an activator)
timestep_negative_node(E,T,N) :- node_regulator(N,C), curated_observation(E,T,C,0), activator(C).
%Variant for variables that are inhibitors
timestep_negative_node(E,T,N) :- node_regulator(N,C), curated_observation(E,T,C,1), inhibitor(C).

%Nodes that aren't negative (i.e. have value 0) at time step T of experiment E must be positive (i.e. have value 1)
timestep_positive_node(E,T,N) :- not timestep_negative_node(E,T,N), node_ID(N), curated_observation(E,T,_,_).

%Determine all positive observations that are covered by the selected nodes (i.e. positive observations that can
%be obtained by those nodes, since the nodes are positive in the timestep prior to those observations)
node_positive_observation_coverage(N,E,T) :- unique_positive_observation(E,T), timestep_positive_node(E,T-1,N).

%If two candidate nodes cover different positive observations, then their behavior is distinct
%(used in integrity constraint #3)
nodes_distinct_coverage(N1,N2) :- node_ID(N1), node_ID(N2), N1 < N2, 
  node_positive_observation_coverage(N1,E,T), not node_positive_observation_coverage(N2,E,T).

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
%We're only interested in generating nodes that can be used to explain the observations,
%which is not possible for a node to do if it is active when we expect it to be inactive
:- timestep_positive_node(E,T-1,N), curated_observation(E,T-1,compound,1), 
  curated_observation(E,T,compound,0), T > 0.

%2-Every positive observation must be covered by some positive node
:- unique_positive_observation(E,T), not node_positive_observation_coverage(_,E,T).

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