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
%The highest number of nodes we'll consider is equal to the number of active observations,
%since at most we'll need one node per active observation to render the model consistent
maximum_nodes(ACTIVE_OBSERVATIONS) :- ACTIVE_OBSERVATIONS = #count{E,T,compound,1 : curated_observation(E,T,compound,1)}.

%If we have at least some observation where the compound is active at a T > 0,
%then we have active observations
active_observations :- curated_observation(_,T,compound,1), time(T), T > 0.

%If we have no active observations, then we will consider as many nodes as there are compounds
%in the model (this should be more than enough, because we want to find a solution that is never active,
%therefore the fewer nodes it has, the more restrictive it can be, and the higher the probability that it is never active.)
maximum_nodes(TOTAL_COMPOUNDS) :- not active_observations, TOTAL_COMPOUNDS = #count{C : node(C)}.

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

%If the compound is active at time T, there must be at least one active node active at time T-1
1{candidate_node(N) : node_active(E,T-1,N)} :- curated_observation(E,T,compound,1), T > 0.

%If we have no observations where the compound is active, then any node can be a candidate node
1{candidate_node(N) : node_(N)} :- not active_observations.


%*--Adding nodes with missing regulators--*%
%If a regulator is part of a node N, then that regulator is present
present(C) :- candidate_node(N), node_regulator(N,C).

%If one of the original regulators is not present in any node, mark it as missing
missing_regulator(C) :- original_regulator(C), not present(C).

%If one of the new regulators is not present in the original set, mark it as an extra
extra_regulator(C) :- not original_regulator(C), present(C).

%Create new nodes for the missing regulators (at most one new node per missing regulator)
missing_node(MN+1..MN+MISSING) :- maximum_nodes(MN), MISSING = #count{C : missing_regulator(C)}.

%If we have a missing regulator, it may or may not belong to some node
{node_regulator(N,C) : missing_node(N)} :- missing_regulator(C).
 
%*--Selecting the final nodes--*%
%Candidate nodes are always part of the final solution 
final_candidate(N) :- candidate_node(N).

%Nodes comprised of missing regulators may or may not be present in the final solution
{final_candidate(N)} :- missing_node(N), node_regulator(N,C).

%*--Calculating the number of missing original regulators in the final solution--*%
final_present(C) :- missing_regulator(C), node_regulator(N,C), final_candidate(N).
final_missing_regulator(C) :- missing_regulator(C), not final_present(C).

%*--Verifying whether the rule that no node can contain another node has been broken (BCF)--*%
%Calculate the number of variables per final node
node_varno(N,N_VARNO) :- N_VARNO = #count{ C : node_regulator(N,C) }, final_candidate(N).

%If the number of variables in one node is equal to the number of variables that it has in common with another node,
%then the first node is fully contained within the second node, and so the BCF has been broken
bcf_broken :- final_candidate(N1), final_candidate(N2), N1 != N2, 
  COMMON = #count{C : node_regulator(N1,C), node_regulator(N2,C)}, node_varno(N1,N1_VARNO), COMMON = N1_VARNO.


%Test
%The chosen final nodes cannot be active when the given compound should be inactive
:- final_candidate(N), node_active(E,T-1,N), curated_observation(E,T,compound,0), T > 0.

%The BCF cannot be broken (nodes cannot contain other nodes)
:- bcf_broken.


%Display
final_node_regulator(N,C) :- final_candidate(N), node_regulator(N,C).
final_activator(C) :- final_node_regulator(N,C), activator(C).
final_inhibitor(C) :- final_node_regulator(N,C), inhibitor(C).
no_solutions :- {final_candidate(N)} = 0.

#show no_solutions/0.
#show final_candidate/1.
#show final_activator/1.
#show final_inhibitor/1.
#show final_node_regulator/2.


%Optimize
%Optimize for the minimum number of final nodes (highest priority)
#minimize{1@3,N : final_candidate(N)}.

%Optimize for the minimum changes to regulators
#minimize{1@2,C : final_missing_regulator(C)}.
#minimize{1@2,C : extra_regulator(C)}.

%Optimize for the minimum changes to regulator signs (lowest priority)
#minimize{1@1,C : sign_changed(C)}.
