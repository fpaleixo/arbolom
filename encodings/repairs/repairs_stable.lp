%Generates the best candidate function for stable state observations
#const compound = c.

%Define
%*--Preliminaries--*%
%Get the original regulators from the inconsistent model
original_regulator(C) :- edge(C,compound,_).

%*--Regulator signs--*%
%A compound can either be an inhibitor or an activator, but not both
1 {activator(C); inhibitor(C)} 1 :- node(C).

%Keep track of which original regulators had their sign changed
sign_changed(C) :- edge(C,compound,0), inhibitor(C).
sign_changed(C) :- edge(C,compound,1), activator(C).

%*--Node creation--*%
%The highest number of nodes we'll consider is equal to the number of unique active observations,
%since at most we'll need one node per unique active observation to render the model consistent
%(it may be that one node can explain several active observations)
maximum_nodes(ACTIVE_OBSERVATIONS) :- ACTIVE_OBSERVATIONS = #count{E,compound : curated_observation(E,compound,1)}.

%If we have at least some observation where the compound is active,
%then we have active observations
active_observations :- curated_observation(_,compound,1).

%If we have no active observations, then we will use 1 node maximum to explain the observations.
%If 1 node isn't enough to produce a function that's restrictive enough, then no such function exists
%(since considering more nodes would never allow us to create more restrictive fuctions, only more general ones)
maximum_nodes(1) :- not active_observations.

%Every node has a unique id in the form of an integer
node_(1..MN) :- maximum_nodes(MN).

%A given compound may or may not belong to some node
{node_regulator(N,C) : node_(N)} :- node(C).

%*--Choosing the candidate nodes--*%
%If one of a node's variables has value 0 for experiment E, 
%then for that same experiment the node will also have value 0 (if that variable is an activator)
node_inactive(E,N) :- node_(N), node_regulator(N,C), curated_observation(E,C,0), activator(C).
%Variant for variables that are inhibitors
node_inactive(E,N) :- node_(N), node_regulator(N,C), curated_observation(E,C,1), inhibitor(C).

%Nodes that aren't inactive in experiment E must be active
node_active(E,N) :- not node_inactive(E,N), node_(N), curated_observation(E,_,_).

%If the compound is active in an experiment E, there must be at least one active node for that experiment
%(the at least one restriction is enforced via minimization -- see lines 82 & 111)
{candidate_node(E,N) : node_active(E,N)} 1 :- curated_observation(E,compound,1).
candidate_node(N) :- candidate_node(E,N).

%Determine all observations that are covered by the selected nodes
node_observation_coverage(N,E) :- curated_observation(E,compound,1), candidate_node(N), node_active(E,N).

%If two candidate nodes cover different active observations, then their behavior is distinct
distinct_behavior(N1,N2) :- candidate_node(N1), candidate_node(N2), N1 < N2, node_observation_coverage(N1,E), not node_observation_coverage(N2,E).

%If we have no observations where the compound is active, then if we have a candidate it can only be node 1
{candidate_node(1)} :- not active_observations.

%*--Marking missing/extra regulators--*%
%If a regulator is part of a node N, then that regulator is present
present(C) :- candidate_node(N), node_regulator(N,C).

%If one of the original regulators is not present in any node, mark it as missing
missing_regulator(C) :- original_regulator(C), not present(C).

%If one of the new regulators is not present in the original set, mark it as an extra
extra_regulator(C) :- not original_regulator(C), present(C).
 
%*--Verifying whether the rule that no node can contain another node has been broken (BCF)--*%
%Calculate the number of variables per candidate node
node_varno(N,N_VARNO) :- N_VARNO = #count{ C : node_regulator(N,C) }, candidate_node(N).

%If the number of variables in one node is equal to the number of variables that it has in common with another node,
%then the first node is fully contained within the second node, and so the BCF has been broken
bcf_broken :- candidate_node(N1), candidate_node(N2), N1 != N2, node_varno(N1,N1_VARNO),
  COMMON = #count{C : node_regulator(N1,C), node_regulator(N2,C)}, COMMON = N1_VARNO.

%*--No solution determination--*%
no_solution :- {candidate_node(N)} = 0.
no_solution :- curated_observation(E,compound,1), not candidate_node(E,_).
no_solution :- node_active(E,1), curated_observation(E,compound,0), not active_observations.


%Test
%We're only interested in generating nodes that can be used to explain the observations,
%which is not possible for a node to do if it is active when we expect it to be inactive
:- node_active(E,N), curated_observation(E,compound,0), active_observations.

%If two candidate nodes share the same behavior, then the solution is not optimal
:- candidate_node(N1), candidate_node(N2), N1 < N2, not distinct_behavior(N1,N2).

%The BCF cannot be broken (nodes cannot contain other nodes)
:- bcf_broken.

%We are only interested in considering nodes that have some regulator
:- node_(N), not node_regulator(N,_).


%Display
final_node_regulator(N,C) :- candidate_node(N), node_regulator(N,C).
final_activator(C) :- final_node_regulator(N,C), activator(C).
final_inhibitor(C) :- final_node_regulator(N,C), inhibitor(C).

#show no_solution/0.
#show candidate_node/1.
#show final_activator/1.
#show final_inhibitor/1.
#show final_node_regulator/2.

%Optimize
%Optimize for minimizing the occurence of the no_solution predicate (highest priority)
#minimize{1@4 : no_solution}.

%Optimize for the minimum number of final nodes
#minimize{1@3,N : candidate_node(N)}.

%Optimize for the minimum changes to regulators
#minimize{1@2,C : missing_regulator(C)}.
#minimize{1@2,C : extra_regulator(C)}.

%Optimize for the minimum changes to regulator signs (lowest priority)
#minimize{1@1,C : sign_changed(C)}.
