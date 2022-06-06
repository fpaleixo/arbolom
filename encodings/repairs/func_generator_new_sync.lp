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
1 {node_candidate(N) : node_active(E,T-1,N)} 1 :- curated_observation(E,T,compound,1), T > 0.

%If a variable is a part of a function candidate node N, then that variable is present
present(V) :- node_candidate(N), node_variable(N,V).

%If a candidate node cannot be found for some variable, mark that variable as missing
missing_variable(V) :- variable(V), not present(V).

%If we have missing variables, add a random candidate with that variable
1 {variable_candidate(V,N) : node_variable(N,V)} 1 :- missing_variable(V).

%Sum of the levels of all node candidates (used for optimization)
total_candidate_level(TL) :- TL = #sum{L,N : node_candidate(N), node_level(N,L)}. 


%Test
%Terms in a function cannot contain any other terms in that function (BCF)
:- node_candidate(N1), node_candidate(N2), edge_(N1,N2).
:- variable_candidate(_,N1), variable_candidate(_,N2), edge_(N1,N2).
:- node_candidate(N1), variable_candidate(_,N2), edge_(N1,N2).


%Display
#show node_candidate/1.
#show variable_candidate/2.


%Optimize
%Optimize for the  highest level possible (the higher the level, the fewer variables per node, so the more general the node)
#maximize{TL: total_candidate_level(TL)}.

