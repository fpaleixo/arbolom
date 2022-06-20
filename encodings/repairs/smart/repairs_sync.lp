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
%since at most we'll need one node per active observation to render the model consistent.
%We include an extra node to accomodate for the possibility of including original
%regulators that don't contribute towards replicating the given observations
maximum_nodes(ACTIVE_OBSERVATIONS + 1) :- ACTIVE_OBSERVATIONS = #count{E,T,compound,1 : curated_observation(E,T,compound,1)}.

%If we have at least some observation where the compound is active at a T > 0,
%then we have active observations
active_observations :- curated_observation(_,T,compound,1), time(T), T > 0.

%If we have no active observations, then we will consider as many nodes as there are compounds
%in the model (this is more than enough, because we want to find a solution that is never active,
%therefore the fewer nodes we use, the more restrictive the solution can be, i.e. the higher the probability that it is never active)
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

%If a node N is active before an inactive observation, then N cannot be a candidate node
inadequate_candidate_node(N) :- node_active(E,T-1,N), curated_observation(E,T,compound,0), T > 0.

%If the compound is active at time T, there must be at least one non-inadequate node active at time T-1 
%(the at least one restriction is enforced via minimization -- see lines 83 & 105)
{candidate_node(E,T,N) : node_active(E,T-1,N), not inadequate_candidate_node(N)} :- curated_observation(E,T,compound,1), T > 0.
candidate_node(N) :- candidate_node(E,T,N).

%If we have no observations where the compound is active, then any non-inadequate node can be a candidate node
{candidate_node(N) : node_(N), not inadequate_candidate_node(N)} :- not active_observations.

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
no_solution :- curated_observation(E,T,compound,1), not candidate_node(E,T,_), T > 0.


%Test
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
