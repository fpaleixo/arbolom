%Generates all possible function candidates for inconsistent functions
%(because we may need to fill in the gaps of incomplete observations, we always need to work
%with all compounds and all observations)

#const compound = c.

%Define
%---Candidate generation---
%Determine the nodes that will be a part of this candidate
1{function_candidate(N) : node_(N), node_variable(N,V) } :- variable(V).

%Clauses in a function cannot contain any other clause in that function (BCF)
:- function_candidate(N1), function_candidate(N2), edge_(N1,N2).


%Display
%#show candidate_nodes/1.
#show function_candidate/1.
%#show term_number/2.
