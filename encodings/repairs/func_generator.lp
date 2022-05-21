%Generates all possible function candidates for inconsistent functions

%Define
%For each candidate level, choose a node for it
1 {function_candidate(C,L,N) : node_(N), node_level(N,L)} 1 :- clause_level(C,L).

%Define simplified predicate to be used in filtering and display
function_candidate(N) :- function_candidate(C,L,N).

%If a variable is a part of a function candidate node N, then that variable is present
present(V) :- function_candidate(N), node_variable(N,V).


%Test
%If there are two candidates with the same level, then the one with the lowest ID always comes first (symmetry breaking)
:-function_candidate(C1,L,N1), function_candidate(C2,L,N2), C2 > C1, N2 <= N1.

%All regulators must be present in the candidate
:- variable(V), not present(V).

%Clauses in a function cannot contain any other clause in that function (BCF)
:- function_candidate(N1), function_candidate(N2), edge_(N1,N2).


%Display
#show function_candidate/1.
