%Generates the best candidate function according to the minimization criteria (one-shot)
#const compound = c.
%TODO force it so that when we have no observations with 1s, a candidate is still produced
%TODO ensure that there is a possibility for more variables to be added even though they may not be possible regulators (handy to minimize regulator changes from the original function)
%TODO add optimization for minimizing number of variable changes

%Define
%A compound can either be an inhibitor or an activator, but not both
1 {activator(C); inhibitor(C)} 1 :- node(C).

%Keep track of which regulators had their sign changed
sign_changed(C) :- edge(C,compound,0), inhibitor(C).
sign_changed(C) :- edge(C,compound,1), activator(C).

%If the compound is active at time T, then whatever compounds are active at time T-1 can be its regulators
possible_regulator(E,T,C) :- curated_observation(E,T,compound,1), curated_observation(E,T-1,C,1), activator(C), T > 0.
possible_regulator(E,T,C) :- curated_observation(E,T,compound,1), curated_observation(E,T-1,C,0), inhibitor(C), T > 0.

%We will never need more nodes than the number of observations where the compound is active
maximum_nodes(MN) :- MN = #count{E,T,compound,1 : curated_observation(E,T,compound,1)}.

%Every node has a unique id in the form of an integer
node_(1..MN) :- maximum_nodes(MN).

%If we have a possible regulator, it may or may not belong to some node
{node_regulator(N,C) : node_(N)} :- possible_regulator(E,T,C).

%If one of a node's variable has value 0 for experiment E at time step T, 
%then for that same experiment and time step the node will also have value 0 (if that variable is an activator)
node_inactive(E,T,N) :- node_(N), node_regulator(N,C), curated_observation(E,T,C,0), activator(C).
%Variant for variables that are inhibitors
node_inactive(E,T,N) :- node_(N), node_regulator(N,C), curated_observation(E,T,C,1), inhibitor(C).

%Nodes that aren't inactive at time step T of experiment E must be active
node_active(E,T,N) :- not node_inactive(E,T,N), node_(N), curated_observation(E,T,_,_).

%If the compound is active at time T, there must be at least one active node active at time T-1
1{final_candidate(N) : node_active(E,T-1,N)} :- curated_observation(E,T,compound,1), T > 0.

%Calculate the number of variables per node
node_varno(N,N_VARNO) :- N_VARNO = #count{ C : node_regulator(N,C) }, final_candidate(N).

%If the number of variables in one node is equal to the number of variables that it has in common with another node,
%then the first node is fully contained within the second node, and so the BCF has been broken
bcf_broken :- final_candidate(N1), final_candidate(N2), N1 != N2, 
  COMMON = #count{C : node_regulator(N1,C), node_regulator(N2,C)}, node_varno(N1,N1_VARNO), COMMON = N1_VARNO.


%Test
%The chosen final nodes cannot be active when the given compound should be inactive
:- final_candidate(N), node_active(E,T-1,N), curated_observation(E,T,compound,0), T > 0.

%There must be some active node for every observation where the compound is active 
%TODO change this to final nodes
:- not node_active(E,T-1,N), node_(N), curated_observation(E,T,compound,1), T > 0.

%The BCF cannot be broken (nodes cannot contain other nodes)
:- bcf_broken.


%Display
final_node_regulator(N,C) :- final_candidate(N), node_regulator(N,C).
final_activator(C) :- final_node_regulator(N,C), activator(C).
final_inhibitor(C) :- final_node_regulator(N,C), inhibitor(C).

#show final_candidate/1.
#show final_node_regulator/2.
#show final_activator/1.
#show final_inhibitor/1.


%Optimize
%Optimize for the minimum number of final nodes (highest priority)
#minimize{1@1,N : final_candidate(N)}.

%Optimize for the minimum changes to regulator signs
#minimize{1@2,V : sign_changed(V)}.