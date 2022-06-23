%Generates the best candidate function according to the minimization criteria (one-shot)
#const compound = c.

%Define
%*--Preliminaries--*%
%Time must occur in some rule head
time(T) :- curated_observation(_,T,_,_).

%Get the original regulators from the inconsistent model
original_regulator(C) :- edge(C,compound,_).

%*--Regulator signs--*%
%A compound can either be an inhibitor or an activator, but not both
1 {activator(C); inhibitor(C)} 1 :- node(C).

%Keep track of which original regulators had their sign changed
sign_changed(C) :- edge(C,compound,0), inhibitor(C).
sign_changed(C) :- edge(C,compound,1), activator(C).

%*--Node creation--*%
%Determine distinct observations that happen before active observations 
%TODO improve this so that only two active observations with the exact same state are compared, as opposed to any two active observations
distinct_observations(E1,T1,E2,T2) :- curated_observation(E1,T1,compound,1), curated_observation(E2,T2,compound,1), 
  curated_observation(E1,T1-1,COMPOUND,S1), curated_observation(E2,T2-1,COMPOUND,S2), S1 != S2, T1 > 0, T2 > 0.

%If the observations that happen before any two given active observations are not distinct, then one is a duplicate of the other
%(two rules are required to ensure that the first observation is never marked as a duplicate, only the ones after it)
duplicate_observation(E2,T2) :- curated_observation(E1,T1,compound,1), curated_observation(E2,T2,compound,1), 
  not distinct_observations(E1,T1,E2,T2), E2 > E1, T1 > 0, T2 > 0.
duplicate_observation(E,T2) :- curated_observation(E,T1,compound,1), curated_observation(E,T2,compound,1), 
  not distinct_observations(E,T1,E,T2), T2 > T1, T1 > 0, T2 > 0.

%The highest number of nodes we'll consider is equal to the number of unique active observations,
%since at most we'll need one node per unique active observation to render the model consistent
%(it may be that one node can explain several active observations)
maximum_nodes(ACTIVE_OBSERVATIONS) :- ACTIVE_OBSERVATIONS = #count{E,T,compound,1 : curated_observation(E,T,compound,1), not duplicate_observation(E,T)}.

%If we have at least some observation where the compound is active at a T > 0,
%then we have active observations
active_observations :- curated_observation(_,T,compound,1), time(T), T > 0.

%If we have no active observations, then we will use 1 node maximum to explain the observations.
%If 1 node isn't enough to produce a function that's restrictive enough, then no such function exists
%(since considering more nodes would never allow us to create more restrictive fuctions, only more general ones)
maximum_nodes(1) :- not active_observations.

%Every node has a unique id in the form of an integer
node_(1..MN) :- maximum_nodes(MN).

%A given compound may or may not belong to some node
{node_regulator(N,C) : node_(N)} :- node(C).

%*--Choosing the candidate nodes--*%
%If one of a node's variables has value 0 for experiment E at time step T, 
%then for that same experiment and time step the node will also have value 0 (if that variable is an activator)
node_inactive(E,T,N) :- node_(N), node_regulator(N,C), curated_observation(E,T,C,0), activator(C).
%Variant for variables that are inhibitors
node_inactive(E,T,N) :- node_(N), node_regulator(N,C), curated_observation(E,T,C,1), inhibitor(C).

%Nodes that aren't inactive at time step T of experiment E must be active
node_active(E,T,N) :- not node_inactive(E,T,N), node_(N), curated_observation(E,T,_,_).

%If the compound is active at time T, there must be at least one node active at time T-1 
%(the at least one restriction is enforced via minimization -- see lines 83 & 105)
{candidate_node(E,T,N) : node_active(E,T-1,N)} 1 :- curated_observation(E,T,compound,1), T > 0, not duplicate_observation(E,T).
candidate_node(N) :- candidate_node(E,T,N).

%Determine all observations that are covered by the selected nodes
node_observation_coverage(N,E,T) :- curated_observation(E,T,compound,1), T > 0, not duplicate_observation(E,T), candidate_node(N), node_active(E,T-1,N).

%If two candidate nodes cover different active observations, then their behavior is distinct
distinct_behavior(N1,N2) :- candidate_node(N1), candidate_node(N2), N1 < N2, node_observation_coverage(N1,E,T), not node_observation_coverage(N2,E,T).

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
no_solution :- curated_observation(E,T,compound,1), not duplicate_observation(E,T), not candidate_node(E,T,_), T > 0.
no_solution :- node_active(E,T-1,1), curated_observation(E,T,compound,0), T > 0, not active_observations.


%Test
%We're only interested in generating nodes that can be used to explain the observations,
%which is not possible for a node to do if it is active when we expect it to be inactive
:- node_active(E,T-1,N), curated_observation(E,T,compound,0), T > 0, active_observations.

%If two candidate nodes share the same behavior, then the solution is not optimal
:- candidate_node(N1), candidate_node(N2), N1 < N2, not distinct_behavior(N1,N2).

%The BCF cannot be broken (nodes cannot contain other nodes)
:- bcf_broken.


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
