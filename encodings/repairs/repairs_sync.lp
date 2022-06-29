%Generates the best candidate function for synchronous observations
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

%*--Identification of identical observation states--*%
%Active observations are observations where the compound is active
active_observation(E,T) :- curated_observation(E,T,compound,1), T > 0.

%If we have at least some observation where the compound is active at a T > 0,
%then we have active observations
active_observations :- active_observation(_,_).

%If two active observations have at least one compound in differing states, they are distinct
distinct_active_observations(E1,T1,E2,T2) :- active_observation(E1,T1), active_observation(E2,T2), 
  curated_observation(E1,T1,COMPOUND,S1), curated_observation(E2,T2,COMPOUND,S2), E2 > E1, S1 != S2, T1 > 0, T2 > 0.
distinct_active_observations(E,T1,E,T2) :- active_observation(E,T1), active_observation(E,T2), 
  curated_observation(E1,T1,COMPOUND,S1), curated_observation(E2,T2,COMPOUND,S2), T2 > T1, S1 != S2, T1 > 0, T2 > 0.

%Two active observations with no compounds in differing states are equal
equal_active_observations(E1,T1,E2,T2) :- active_observation(E1,T1), active_observation(E2,T2), 
  not distinct_active_observations(E1,T1,E2,T2), T1 > 0, T2 > 0, E2 > E1.
equal_active_observations(E,T1,E,T2) :- active_observation(E,T1), active_observation(E,T2), 
  not distinct_active_observations(E,T1,E,T2), T1 > 0, T2 > 0, T2 > T1.

%If two equal active observations have previous observations that are not equal to one another, then we have distinct model states
distinct_state_equal_observations(E1,T1,E2,T2) :- equal_active_observations(E1,T1,E2,T2), 
  curated_observation(E1,T1-1,COMPOUND,S1), curated_observation(E2,T2-1,COMPOUND,S2), S1 != S2.

%If two equal active observations have previous observations that are also equal, then both describe the same state
duplicate_state(E2,T2) :- equal_active_observations(E1,T1,E2,T2), not distinct_state_equal_observations(E1,T1,E2,T2).

%If an active observation does not belong to a duplicate state, then it is unique
unique_active_state(E,T) :- active_observation(E,T), not duplicate_state(E,T).

%*--Node creation--*%
%The highest number of nodes we'll consider is equal to the number of unique active observations,
%since at most we'll need one node per unique active observation to render the model consistent
%(it may be that one node can explain several active observations)
maximum_nodes(ACTIVE_OBSERVATIONS) :- ACTIVE_OBSERVATIONS = #count{E,T,compound,1 : unique_active_state(E,T)}.

%If we have no active observations, then we will use 1 node maximum to explain the observations.
%If 1 node isn't enough to produce a function that's restrictive enough, then no such function exists
%(since considering more nodes would never allow us to create more restrictive fuctions, only more general ones)
maximum_nodes(1) :- not active_observations.

%Define all possible node IDs (needed to ensure integrity constraint #1 has no unsafe variables)
possible_node_ID(1..MN) :- maximum_nodes(MN).

%Generate the node IDs of the final solution
1 {node_ID(1..MN)} MN :- maximum_nodes(MN).

%Distribute regulators between the generated nodes
{node_regulator(N,C) : node_ID(N)} :- node(C).

%*--Choosing the candidate nodes--*%
%If one of a node's variables has value 0 for experiment E at time step T, 
%then for that same experiment and time step the node will also have value 0 (if that variable is an activator)
node_inactive(E,T,N) :- node_ID(N), node_regulator(N,C), curated_observation(E,T,C,0), activator(C).
%Variant for variables that are inhibitors
node_inactive(E,T,N) :- node_ID(N), node_regulator(N,C), curated_observation(E,T,C,1), inhibitor(C).

%Nodes that aren't inactive at time step T of experiment E must be active
node_active(E,T,N) :- not node_inactive(E,T,N), node_ID(N), curated_observation(E,T,_,_).

%Determine all observations that are covered by the selected nodes
node_observation_coverage(N,E,T) :- unique_active_state(E,T), node_ID(N), node_active(E,T-1,N).

%If two candidate nodes cover different active observations, then their behavior is distinct
distinct_behavior(N1,N2) :- node_ID(N1), node_ID(N2), N1 < N2, node_observation_coverage(N1,E,T), not node_observation_coverage(N2,E,T).

%*--Marking missing/extra regulators--*%
%If a regulator is part of a node N, then that regulator is present
present(C) :- node_ID(N), node_regulator(N,C).

%If one of the original regulators is not present in any node, mark it as missing
missing_regulator(C) :- original_regulator(C), not present(C).

%If one of the new regulators is not present in the original set, mark it as an extra
extra_regulator(C) :- not original_regulator(C), present(C).
 
%*--Verifying whether the rule that no node can contain another node has been broken (BCF)--*%
%Calculate the number of variables per candidate node
node_varno(N,N_VARNO) :- N_VARNO = #count{ C : node_regulator(N,C) }, node_ID(N).

%If the number of variables in one node is equal to the number of variables that it has in common with another node,
%then the first node is fully contained within the second node, and so the BCF has been broken
bcf_broken :- node_ID(N1), node_ID(N2), N1 != N2, node_varno(N1,N1_VARNO),
  COMMON = #count{C : node_regulator(N1,C), node_regulator(N2,C)}, COMMON = N1_VARNO.


%Test
%Nodes must be created in ordered of IDs (symmetry breaking)
:- node_ID(N2), not node_ID(N1), possible_node_ID(N1), N2 > N1.

%We are only interested in considering nodes that have some regulator
:- node_ID(N), not node_regulator(N,_).

%We're only interested in generating nodes that can be used to explain the observations,
%which is not possible for a node to do if it is active when we expect it to be inactive
:- node_active(E,T-1,N), curated_observation(E,T,compound,0), T > 0.

%Every positive observation must be covered by some node
:- unique_active_state(E,T), not node_observation_coverage(_,E,T).

%If two candidate nodes share the same behavior, then the solution is not optimal
:- node_ID(N1), node_ID(N2), N1 < N2, not distinct_behavior(N1,N2).

%The BCF cannot be broken (nodes cannot contain other nodes)
:- bcf_broken.


%Display
final_node_regulator(N,C) :- node_ID(N), node_regulator(N,C).
final_activator(C) :- final_node_regulator(N,C), activator(C).
final_inhibitor(C) :- final_node_regulator(N,C), inhibitor(C).

#show node_ID/1.
#show final_activator/1.
#show final_inhibitor/1.
#show final_node_regulator/2.

%Optimize
%Optimize for the minimum number of final nodes (highest priority)
#minimize{1@3,N : node_ID(N)}.

%Optimize for the minimum changes to regulators
#minimize{1@2,C : missing_regulator(C)}.
#minimize{1@2,C : extra_regulator(C)}.

%Optimize for the minimum changes to regulator signs (lowest priority)
#minimize{1@1,C : sign_changed(C)}.
