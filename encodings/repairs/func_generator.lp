%Generates all possible function candidates for inconsistent functions

%TODO - filter candidates

%Define
%How many nodes there will be in a given candidate (used to ensure we are generating all candidates with
%1,2,...,MAX nodes possible)
{candidate_nodes(1..MAX_NODES)} = 1 :- total_variables(TV), MAX_NODES = @combination(TV,TV/2).

%For the chosen number of nodes, create a function candidate with as many nodes as that number
{function_candidate(N) : node_(N)} = MN:- candidate_nodes(MN).

%If a variable (regulator) is a part of the function candidate, then it is present
present(V) :- function_candidate(N), node_variable(N,V), variable(V).


%Test 
%Since we are considering non-degenerate functions, all regulators must be present in the candidate
:- variable(V), not present(V).

%Clauses in a function cannot contain any other clause in that function (BCF)
:- function_candidate(N1), function_candidate(N2), edge_(N1,N2).


%Display
#show function_candidate/1.