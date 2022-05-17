%Filters candidate functions according to stable state observations

#const compound = c.

%Define
%Choose a node to be a function candidate
{function_candidate(N)} :- node_(N).

%A node with no regulatory function is an input node
input_node(N) :- node(N), not function(N,_), N != compound.

%Input nodes can take any value
0 {active(E,N)} 1 :- experiment(E), input_node(N).

%For a given node N with I implicants, if there exists a regulator in implicant number I_NO
%which is an inactive activator (outputs 1 when active) in an obervation E, then implicant 
%I_NO evaluates to 0 for that observation E, and so is inactive
implicant_inactive(E,N,I_NO) :- function(N,I), term(N,I_NO,R), edge(R,N,0), curated_observation(E,R,0).
%Variant for generated candidates
candidate_node_inactive(E,N,C) :- N = compound, function_candidate(C), node_variable(C,V), edge(V,N,0), curated_observation(E,V,0).

%For a given node N with I implicants, if there exists a regulator in implicant number I_NO
%which is an active inhibitor (outputs 1 when inactive) in an obervation E at time step T, then implicant 
%I_NO evaluates to 0 for that observation E, and so is inactive
implicant_inactive(E,N,I_NO) :- function(N,I), term(N,I_NO,R), edge(R,N,1), curated_observation(E,R,1).
%Variant for generated candidates
candidate_node_inactive(E,N,C) :- N = compound, function_candidate(C), node_variable(C,V), edge(V,N,1), curated_observation(E,V,1).

%For a given node N with I implicants, if for experiment E there exists
%some implicant which is not inactive, then N has at least one active implicant and so is active
active(E,N) :- function(N,I), not implicant_inactive(E,N,I_NO), experiment(E), term(N,I_NO,_).
%Variant for generated candidates
active(E,N) :- N = compound, function_candidate(C), not candidate_node_inactive(E,N,C), experiment(E).

%If node  N is active but there is an observation stating it should be inactive, then the model is inconsistent
inconsistent(E,N,1) :- active(E,N), curated_observation(E,N,0), N=compound.

%If compound N is inactive but there is an observation stating it should be active, then the model is inconsistent
inconsistent(E,N,0) :- not active(E,N), curated_observation(E,N,1), N=compound.


%Test
%Only one node can be a function candidate (one answer set per node)
:- #count{N : function_candidate(N)} != 1.

%Input nodes need to take values consistent with the observations (when they exist)
:- curated_observation(E,N,0), active(E,N), input_node(N).
:- curated_observation(E,N,1), not active(E,N), input_node(N).

%There can be no inconsistent atoms where the chosen node produces a 1 when 0 was expected
:-inconsistent(E,N,1), N = compound.


%Display 
%Format chosen node for display
filtered_node_(N) :- function_candidate(N).
filtered_node_variable(N,V) :- filtered_node_(N), node_variable(N,V).

#show filtered_node_/1.
#show filtered_node_variable/2.
