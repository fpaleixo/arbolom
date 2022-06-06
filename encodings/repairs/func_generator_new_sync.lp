%Generates candidate functions using observations.
#const compound = c.

%Define
%Time must occur in some rule head
time(T) :- curated_observation(_,T,_,_).

%If one of a node's variable has value 0 for experiment E at time step T, 
%then for that same experiment and time step the node will also have value 0 (if that variable is an activator)
node_inactive(E,T,N) :- node_(N), node_variable(N,V), curated_observation(E,T,V,0), edge(V,compound,0).
%Variant for variables that are inhibitors
node_inactive(E,T,N) :- node_(N), node_variable(N,V), curated_observation(E,T,V,1), edge(V,compound,1).

%Nodes that aren't inactive at time step T of experiment E must be active
node_active(E,T,N) :- not node_inactive(E,T,N), node_(N), curated_observation(E,T,_,_).

%Every observation in which the given compound is active needs to be covered by some node
%TODO this is not enough. it may be that all 1s are covered by some node, but that we do not have enough 1s to be able to get a consistent candidate.
%TODO we will need to somehow come up with a way to generate more candidates despite this...
1 {function_candidate(N) : node_active(E,T-1,N)} 1 :- curated_observation(E,T,compound,1), T > 0.

%If a variable is a part of a function candidate node N, then that variable is present
present(V) :- function_candidate(N), node_variable(N,V).

%Function candidates are final candidates
final_candidate(N) :- function_candidate(N).

%!If cannot find a candidate node for some variable, mark that variable as missing
%missing_variable(V) :- variable(V), not present(V).

%!If we have missing variables, add a candidate with that variable
%{variable_candidate(V,N) : node_variable(N,V)} 1 :- missing_variable(V).

%!Variable candidates are final candidates
%final_candidate(N) :- variable_candidate(V,N).

%If no candidates were found, output no_candidates 
no_candidates :- total_candidates(T), T = 0.

%!If no nodes could be found for missing variables, output no_candidates
%no_candidates :- missing_variable(V), not variable_candidate(V,_).

%Total number of candidate nodes (used for optimization)
total_candidates(T) :- T = #count{N : final_candidate(N)}.

%Sum of the levels of all candidate nodes (used for optimization)
total_candidate_level(TL) :- TL = #sum{L,N : final_candidate(N), node_level(N,L)}. 

%Test
%Terms in a function cannot contain any other terms in that function (BCF)
:- final_candidate(N1), final_candidate(N2), edge_(N1,N2).


%Display
#show final_candidate/1.
%#show function_candidate/1.
%#show variable_candidate/2.
%#show missing_variable/1.
%#show no_candidates/0.
%#show node_active/3.


%Optimize
%Optimize for the most general function possible (i.e. highest number of terms, highest level possible (the higher the level, the fewer variables per node))
#maximize{T : total_candidates(T)}.
#maximize{TL: total_candidate_level(TL)}.

