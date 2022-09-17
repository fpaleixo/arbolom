%Generates the best candidate function for stable state observations.
%(In stable state mode we must ensure that, given the values of a compound's
%regulators, the compound is able to replicate its observed state).

#const compound = c.
#const node_number = n.

%*--Fixing regulators--*%
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

%*--Creating nodes--*%
%Original node IDs must always be available 
%(so that we are able to make as little changes to the format of the original 
%nodes as possible, using optimizations #3). Note that we cannot simply 
%create all IDs using 1..node_number, since node_number may be smaller than
%the number of original nodes. This would cause us to potentially leave out 
%some original nodes when optimizing the format of our solution nodes
available_node_ID(1..TERM_NO) :- function(compound, TERM_NO).

%If we require more IDs than those that were originally available,
%create them
available_node_ID(TERM_NO + 1..node_number):- function(compound, TERM_NO), node_number > TERM_NO.

%Distribute compounds across available IDs
{node_regulator(N,C) : compound(C)} :- available_node_ID(N).

%Project the node IDs our solution is using into their own predicate
node_ID(N) :- node_regulator(N,_).

%*--Assessing node behavior--*%
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
 
%*--Verifying whether the rule that no node can contain another node has been broken (BCF)--*%
%Calculate the number of regulators per candidate node
node_regulator_number(N,N_VARNO) :- N_VARNO = #count{ C : node_regulator(N,C) }, node_ID(N).

%If the number of variables in one node is equal to the number of variables that it has in common with another node,
%then the first node is fully contained within the second node, and so the BCF has been broken
bcf_broken :- node_ID(N1), node_ID(N2), N1 != N2, node_regulator_number(N1,N1_VARNO),
  COMMON_VARNO = #count{C : node_regulator(N1,C), node_regulator(N2,C)}, COMMON_VARNO = N1_VARNO.

%*--Identifying missing/extra regulators (minimization #1)--*%
%An original_regulator C is a regulator that is present in the original inconsistent function
original_regulator(C) :- regulates(C,compound,_).

%If a regulator C is present in node N, then we define it as a present_regulator
present_regulator(C) :- node_regulator(N,C).

%If an original regulator C is not present in any node, we define it as a missing_regulator
missing_regulator(C) :- original_regulator(C), not present_regulator(C).

%If a present regulator C is not one of the original regulators, we define it as an extra_regulator
extra_regulator(C) :- not original_regulator(C), present_regulator(C).

%*--Identifying sign changes (minimization #2)--*%
%(used in minimization #2)
sign_changed(C) :- regulates(C,compound,0), inhibitor(C).
sign_changed(C) :- regulates(C,compound,1), activator(C).

%*--Identifying node format changes (optimizations #3)--*%
%If we have a regulator R in term ID of compound's original function, but our
%solution does not have regulator R in the node with the same ID, then that node
%has a missing regulator
missing_node_regulator(ID,R) :- term(compound, ID, R), node_ID(ID), not node_regulator(ID, R).

%If we have a regulator R in node ID, but our original function does not have 
%regulator R in the term with the same ID, then that node has an
%extra regulator
extra_node_regulator(ID,R) :- node_regulator(ID, R), term(compound, ID, _), not term(compound, ID, R).


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

%6-We must always have node_number nodes in our solution
:- node_number != #count{N : node_regulator(N,R)}.

%7-If we are searching for functions with a fewer or equal number of nodes 
%than the original, then all the IDs we use must be IDs of the original nodes
:- node_number <= TERM_NO, function(compound, TERM_NO), node_ID(N), N > TERM_NO.

%8-If we are searching for functions with a greater number of nodes 
%than the original, then all of the original IDs must be present
:- node_number > TERM_NO, function(compound, TERM_NO), term(compound,N,_), not node_ID(N).


%Display
regulator_activator(C) :- node_regulator(N,C), activator(C).
regulator_inhibitor(C) :- node_regulator(N,C), inhibitor(C).

#show node_ID/1.
#show regulator_activator/1.
#show regulator_inhibitor/1.
#show node_regulator/2.

#show missing_regulator/1.
#show extra_regulator/1.
#show sign_changed/1.
#show missing_node_regulator/2.
#show extra_node_regulator/2.


%Optimize
%1-Optimize for the minimum changes to regulators (highest priority)
#minimize{1@3,C : missing_regulator(C)}.
#minimize{1@3,C : extra_regulator(C)}.

%2-Optimize for the minimum changes to regulator signs 
#minimize{1@2,C : sign_changed(C)}.

%3-Optimize for minimum changes to original node format
#minimize{1@1,N,C : missing_node_regulator(N,C)}.
#minimize{1@1,N,C : extra_node_regulator(N,C)}.
