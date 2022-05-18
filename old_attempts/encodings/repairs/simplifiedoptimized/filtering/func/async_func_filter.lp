%Filters candidate functions according to asynchronous time-series observations

#const compound = c.

%Define
%Time must occur in some rule head
time(T) :- curated_observation(_,T,_,_).

%A node with no regulatory function is an input node (can take any value)
input_node(N) :- node(N), not function(N,_), N != compound.

%Input nodes can take any value
0 {active(E,T,N)} 1 :- experiment(E), time(T), input_node(N).

%For a given node N with I implicants, if there exists a regulator in implicant number I_NO
%which is an inactive activator (outputs 1 when active) in an observation E at time T, then implicant 
%I_NO evaluates to 0 for that observation E at time T, and so is inactive at time T
implicant_inactive(E,T,N,I_NO) :- function(N,I), term(N,I_NO,R), edge(R,N,0), curated_observation(E,T,R,0).
%Variant for generated candidates
candidate_node_inactive(E,T,N,C) :- N = compound, function_candidate(C), node_variable(C,V), edge(V,N,0), curated_observation(E,T,V,0).

%For a given node N with I implicants, if there exists a regulator in implicant number I_NO
%which is an active inhibitor (outputs 1 when inactive) in an observation E at time T, then implicant 
%I_NO evaluates to 0 for that observation E at time T, and so is inactive at time T
implicant_inactive(E,T,N,I_NO) :- function(N,I), term(N,I_NO,R), edge(R,N,1), curated_observation(E,T,R,1).
%Variant for generated candidates
candidate_node_inactive(E,T,N,C) :- N = compound, function_candidate(C), node_variable(C,V), edge(V,N,1), curated_observation(E,T,V,1).

%For a given node N with I implicants, if for experiment E at time T there exists
%some implicant I_NO which is not inactive, then N has at least one active implicant at time T and so will be active at time T+1
active(E,T+1,N) :- function(N,I), not implicant_inactive(E,T,N,I_NO), experiment(E), term(N,I_NO,_), time(T).
%Variant for generated candidates
active(E,T+1,N) :- N = compound, function_candidate(C), not candidate_node_inactive(E,T,N,C), experiment(E), time(T).

%If a node's state has been changed from time T to T+1, identify that node
changed_node(E,T,N) :- curated_observation(E,T,N,S1), curated_observation(E,T+1,N,S2), S1 != S2, not input_node(N).

%If node  N is active but there is an observation stating it should be inactive, then the model is inconsistent
inconsistent(E,T,N,1) :- changed_node(E,T-1,N), active(E,T,N), curated_observation(E,T,N,0), T > 0, N=compound.

%If compound N is inactive but there is an observation stating it should be active, then the model is inconsistent
inconsistent(E,T,N,0) :- changed_node(E,T-1,N), not active(E,T,N), curated_observation(E,T,N,1), T > 0, N=compound.

%In asynchronous mode, only one node state may change at each time step (without counting input nodes)
inconsistent(E,T,N1,N2) :- changed_node(E,T,N1), changed_node(E,T,N2), N1 != N2, N1=compound.


%Test
%Input nodes need to take values consistent with the observations (when they exist)
:- curated_observation(E,T,N,0), active(E,T,N), input_node(N).
:- curated_observation(E,T,N,1), not active(E,T,N), input_node(N).

%There can be no inconsistent atoms
:- inconsistent(E,T,N,_), N = compound.
