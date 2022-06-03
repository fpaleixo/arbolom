%Generates candidate functions using observations.
#const compound = c.

%Define
%If one of a node's variables has value 0 for experiment E at time step T, 
%then for that same experiment and time step the node will also have value 0
node_inactive(E,T,N) :- node_(N), node_variable(N,V), curated_observation(E,T,V,0).

%Nodes that aren't inactive at time step T of experiment E must be active
node_active(E,T,N) :- not node_inactive(E,T,N).

%Every observation in which the given compound is active needs to be covered by some node
1 {function_candidate(N) : node_active(E,T,N)} 1 :- curated_observation(E,T,compound,1).

%If a variable is a part of a function candidate node N, then that variable is present
present(V) :- function_candidate(N), node_variable(N,V).


%Test
%All regulators must be present in the candidate
:- variable(V), not present(V).

%Terms in a function cannot contain any other terms in that function (BCF)
:- function_candidate(N1), function_candidate(N2), edge_(N1,N2).


%Display
#show function_candidate/1.


%Optimize
%TODO Optimize for the most general function possible (i.e. highest number of terms, lowest number of variables per term 
%TODO -- for the lowest number of variables, we can use still use the notion of level. The higher the level of a term, the lowest number of variables in that term.)

