%Generates all possible function candidates for inconsistent functions
%(because we may need to fill in the gaps of incomplete observations, we always need to work
%with all compounds and all observations)

%TODO - get original LP, take out inconsistent function; transform candidate into standard function format; filter candidate
#const compound = c.

%Define
%---Candidate generation---
%How many nodes there will be in a given candidate (used to ensure we are generating all candidates with
%1,2,...,MAX nodes possible)
{candidate_nodes(1..MAX_NODES)} = 1 :- total_variables(TV), MAX_NODES = @combination(TV,TV/2).

%For the chosen number of nodes, create a function candidate with as many nodes as that number
{function_candidate(N) : node_(N)} = MN:- candidate_nodes(MN).

%If a variable (regulator) is a part of the function candidate, then it is present
present(V) :- function_candidate(N), node_variable(N,V), variable(V).

%---Candidate convertion---
%Convert candidate into standard format
{term_number(N,1..MN) : candidate_nodes(MN)} = 1 :- function_candidate(N).
function(compound, MN) :- candidate_nodes(MN).
term(compound,TERM_NO,V) :- term_number(N,TERM_NO), node_variable(N,V).

%---Candidate filtering---
%TODO


%Test 
%---Candidate generation---
%Since we are considering non-degenerate functions, all regulators must be present in the candidate
:- variable(V), not present(V).

%Clauses in a function cannot contain any other clause in that function (BCF)
:- function_candidate(N1), function_candidate(N2), edge_(N1,N2).

%---Candidate convertion---
%Different nodes must belong to different function terms
:- term_number(N1,TN1), term_number(N2,TN1), N1 != N2.

%Force an order in term numbers to ensure we aren't getting multiple answer sets
%for the same solution
:- function_candidate(N1), function_candidate(N2), N2 > N1, 
  term_number(N1,TN1), term_number(N2,TN2), TN1 > TN2.

%---Candidate filtering---
%TODO


%Display
function_result(compound,TN) :- function(compound,TN).
term_result(compound,T,V) :- term(compound,T,V).

%#show candidate_nodes/1.
%#show function_candidate/1.
%#show term_number/2.
#show function_result/2.
#show term_result/3.