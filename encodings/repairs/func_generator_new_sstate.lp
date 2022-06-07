%Generates candidate functions using observations.
#const compound = c.

%Define

%If one of a node's variable has value 0 for experiment E at time step T, 
%then for that same experiment and time step the node will also have value 0 (if that variable is an activator)
node_inactive(E,N) :- node_(N), node_variable(N,V), curated_observation(E,V,0), edge(V,compound,0).
%Variant for variables that are inhibitors
node_inactive(E,N) :- node_(N), node_variable(N,V), curated_observation(E,V,1), edge(V,compound,1).

%Nodes that aren't inactive at time step T of experiment E must be active
node_active(E,N) :- not node_inactive(E,N), node_(N), curated_observation(E,_,_).

%Every observation in which the given compound is active needs to be covered by some node
1 {node_candidate(N) : node_active(E,N)} 1 :- curated_observation(E,compound,1).

%If a variable is a part of a function candidate node N, then that variable is present
present(V) :- node_candidate(N), node_variable(N,V).

%If a candidate node cannot be found for some variable, mark that variable as missing
missing_variable(V) :- variable(V), not present(V).

%If we have missing variables, add a random candidate with that variable
1 {variable_candidate(V,N) : node_variable(N,V)} 1 :- missing_variable(V).

%Both node candidates as well as variable candidates are part of our final candidate
final_candidate(N) :- node_candidate(N).
final_candidate(N) :- variable_candidate(V,N).


%Test
%Terms in a function cannot contain any other terms in that function (BCF)
:- final_candidate(N1), final_candidate(N2), edge_(N1,N2).


%Display
#show final_candidate/1.


%Optimize
%Optimize for the minimum number of final nodes
#minimize{1,N : final_candidate(N)}.

