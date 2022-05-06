%Filters candidate functions according to stable state observations

#const compound = c.

%Define
%A node with no regulatory function is an input node
input_node(N) :- node(N), not function(N,_).

%Input nodes can take any value
0 {active(E,N)} 1 :- experiment(E), input_node(N).

%Input observations are converted to curated observations
curated_observation(E,N,0) :- observation(E,N,0).
curated_observation(E,N,1) :- observation(E,N,1).

%If node N is active and there is no observation for it, fill in the missing observation
curated_observation(E,N,1) :- active(E,N), not observation(E,N,_).

%If node N is inactive and there is no observation for it, fill in the missing observation
curated_observation(E,N,0) :- not active(E,N), not observation(E,N,_), experiment(E), node(N).

%For a given node N with I implicants, if there exists a regulator in implicant number I_NO
%which is an inactive activator (outputs 1 when active) in an obervation E, then implicant 
%I_NO evaluates to 0 for that observation E, and so is inactive
implicant_inactive(E,N,I_NO) :- function(N,I), term(N,I_NO,R), edge(R,N,0), curated_observation(E,R,0).

%For a given node N with I implicants, if there exists a regulator in implicant number I_NO
%which is an active inhibitor (outputs 1 when inactive) in an obervation E at time step T, then implicant 
%I_NO evaluates to 0 for that observation E, and so is inactive
implicant_inactive(E,N,I_NO) :- function(N,I), term(N,I_NO,R), edge(R,N,1), curated_observation(E,R,1).

%For a given node N with I implicants, if for experiment E there exists
%some implicant which is not inactive, then N has at least one active implicant and so is active
active(E,N) :- function(N,I), not implicant_inactive(E,N,I_NO), experiment(E), term(N,I_NO,_).

%If node  N is active but there is an observation stating it should be inactive, then the model is inconsistent
inconsistent(E,N,1) :- active(E,N), curated_observation(E,N,0), N=compound.

%If compound N is inactive but there is an observation stating it should be active, then the model is inconsistent
inconsistent(E,N,0) :- not active(E,N), curated_observation(E,N,1), N=compound.


%Test
%Input nodes need to take values consistent with the observations (when they exist)
:- curated_observation(E,N,0), active(E,N), input_node(N).
:- curated_observation(E,N,1), not active(E,N), input_node(N).

%There can be no inconsistent atoms
:-inconsistent(E,N,_).