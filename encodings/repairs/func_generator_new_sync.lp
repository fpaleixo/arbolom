%Generates candidate functions using observations.
#const compound = c.

%Define
%If one of a node's variable has value 0 for experiment E at time step T, 
%then for that same experiment and time step the node will also have value 0 (if that variable is an activator)
node_inactive(E,T,N) :- node_(N), node_variable(N,V), curated_observation(E,T,V,0), edge(V,compound,0).
%Variant for variables that are inhibitors
node_inactive(E,T,N) :- node_(N), node_variable(N,V), curated_observation(E,T,V,1), edge(V,compound,1).

%Nodes that aren't inactive at time step T of experiment E must be active
node_active(E,T,N) :- not node_inactive(E,T,N), node_(N), curated_observation(E,T,_,_).

%Every observation in which the given compound is active needs to be covered by some node
1 {function_candidate(N) : node_active(E,T-1,N)} 1 :- curated_observation(E,T,compound,1), T > 0.

%If a variable is a part of a function candidate node N, then that variable is present
present(V) :- function_candidate(N), node_variable(N,V).

%Total number of candidate nodes (used for optimization)
total_candidates(T) :- T = #count{N : function_candidate(N)}.

%Sum of the levels of all candidate nodes
total_candidate_level(TL) :- TL = #sum{L,N : function_candidate(N), node_level(N,L)}. 


%Test
%All regulators must be present in the candidate
:- variable(V), not present(V).

%Terms in a function cannot contain any other terms in that function (BCF)
:- function_candidate(N1), function_candidate(N2), edge_(N1,N2).


%Display
#show function_candidate/1.


%Optimize
%Optimize for the most general function possible (i.e. highest number of terms, highest level possible (the higher the level, the fewer variables per node))
#maximize{T : total_candidates(T)}.
#maximize{TL: total_candidate_level(TL)}.

