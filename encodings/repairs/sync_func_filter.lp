%Filters candidate functions according to synchronous time-series observations

#const compound = c.

%Define
%Time must occur in some rule head
time(T) :- observation(_,T,_,_).

%A node with no regulatory function is an input node (can take any value)
input_node(N) :- node(N), not function(N,_), N != compound.

%Input nodes can take any value
0 {active(E,T,N)} 1 :- experiment(E), time(T), input_node(N).

%Input observations are converted to curated observations
curated_observation(E,T,N,0) :- observation(E,T,N,0).
curated_observation(E,T,N,1) :- observation(E,T,N,1).

%If node N is active at time T and there is no observation for it, fill in the missing observation
curated_observation(E,T,N,1) :- active(E,T,N), not input_node(N), not observation(E,T,N,_), time(T), experiment(E), node(N).

%If node N is inactive at time T and there is no observation for it, fill in the missing observation
curated_observation(E,T,N,0) :- not active(E,T,N), not input_node(N), not observation(E,T,N,_), time(T), experiment(E), node(N).

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

%If node N is active but there is an observation stating it should be inactive, then the model is inconsistent
inconsistent(E,T,N,1) :- active(E,T,N), curated_observation(E,T,N,0), T > 0, N=compound.

%If compound N is inactive but there is an observation stating it should be active, then the model is inconsistent
inconsistent(E,T,N,0) :- not active(E,T,N), curated_observation(E,T,N,1), T > 0, N=compound.

%Test
%Input nodes need to take values consistent with the observations (when they exist)
:- curated_observation(E,T,N,0), active(E,T,N), input_node(N).
:- curated_observation(E,T,N,1), not active(E,T,N), input_node(N).

%There can be no inconsistent atoms
:-inconsistent(E,T,N,_), N = compound.