%Generates all possible function candidates for inconsistent functions
%(because we may need to fill in the gaps of incomplete observations, we always need to work
%with all compounds and all observations)

%TODO - basically, we'll generate candidates using time steps. the first time-step
%TODO chooses a candidate that ensures that we're on a level that is smaller/greater/the same as the current level
%TODO then, the next time step chooses another candidate that does the same, until at least all variables have a place

#const compound = c.

%Define
term_(1..TN) :- function(F,TN).

0 {function_candidate(T,N) :- node_level(N,LN), func_level(T,LF), LN <= LF} 1 :- term_(T).

%Determine the nodes that will be a part of this candidate
1{function_candidate(N) : node_(N), node_variable(N,V) } :- variable(V).


%Test
%Symmetry breaking - candidates must be ordered by their level
:- function_candidate(T1,N1), node_level(N1,LN1), function_candidate(T2,N2), node_level(N2, LN2), T1 < T2, LN1 > LN2.

%Symmetry breaking - when two chosen nodes have the same level, the one with the smallest ID is always chosen first
:- function_candidate(T1,N2), node_level(N2, LN2), function_candidate(T2,N1), node_level(N2, LN2), 
  T1 < T2, N1 < N2, LN1 = LN2.

%Display
%#show candidate_nodes/1.
#show function_candidate/1.
%#show term_number/2.
