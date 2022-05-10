%Generates all possible function candidates for inconsistent functions
%(because we may need to fill in the gaps of incomplete observations, we always need to work
%with all compounds and all observations)

#const compound = c.

%Define
%---Candidate generation---
%Determine the nodes that will be a part of this candidate
{function_candidate(N) : node_(N)}.

%If a variable (regulator) is a part of the function candidate, then it is present
present(V) :- function_candidate(N), node_variable(N,V), variable(V).


%Test 
%---Candidate generation---
%Since we are considering non-degenerate functions, all regulators must be present in the candidate
:- variable(V), not present(V).

%Clauses in a function cannot contain any other clause in that function (BCF)
:- function_candidate(N1), function_candidate(N2), edge_(N1,N2).


%Display
%#show candidate_nodes/1.
#show function_candidate/1.
%#show term_number/2.
