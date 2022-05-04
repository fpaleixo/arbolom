%Generates all possible function candidates for inconsistent functions

%! DEPRECATED
%! DEPRECATED
%! DEPRECATED

%Define
%Choose the function to generate terms for (only one per answer set, as enforced by the IC below)
{inconsistent_function(F)} :- total_variables(F,T).

%How many clauses(terms) there will be in a given candidate (used to ensure we are generating all candidates with
%1,2,...,MAX terms possible)
{candidate_clauses(F,1..MAX_TERMS)} = 1 :- total_variables(F,T), MAX_TERMS = @combination(T,T/2), inconsistent_function(F).

%For the chosen number of clauses, create a function candidate with as many clauses as that number
{function_candidate(F,CN,L,C) : clause(F,L,C)} = CN:- candidate_clauses(F,CN).

%Clause C1 of level L1 is not contained in clause C2 of level L2 (necessary because
%we're only interested in generating function candidates in the BCF form, which is the disjunction
%of prime implicants. If a clause C1 is contained inside of another clause C2, then C2 is not a prime implicant,
%and therefore cannot be in the same function as C1.)
not_contained_in(F,L1,C1,L2,C2) :- clause(F,L1,C1), clause(F,L2,C2), generated_term(F,L1,C1,N), not generated_term(F,L2,C2,N), L2 > L1.

%If a term is a part of the function candidate, then it is present
present(F,N) :- function_candidate(F,CN,L,C), generated_term(F,L,C,N).

%Test 
%Only one function can be chosen in each answer set (to avoid duplicated generated terms, 
%e.g. generated_term(f1,1,a), generated_term(f2,1,a) in one answer set and generated_term(f1,1,a), generated_term(f2,1,b) in another)
:- #count{F : inconsistent_function(F)} != 1.

%Since we are considering non-degenerate functions, all regulators of F must be present in the candidate
:- generated_term(F,_,_,N), not present(F,N), inconsistent_function(F).

%Clauses in a function cannot contain any other clause in that function (BCF)
:- function_candidate(F,CLAUSE_NUMBER,L1,C1), function_candidate(F,CLAUSE_NUMBER,L2,C2), not not_contained_in(F,L1,C1,L2,C2), L2 > L1.

%Display
#show function_candidate/4.