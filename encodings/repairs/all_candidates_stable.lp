%Repair strategy: For each inconsistent node, generate all possible function candidates.
%Reject candidates which are not able to replicate expected behavior.
%TODO fix term generation bottleneck - with 10 variables takes around 78s, out of which 71s are for solving
#const max_candidates = 18. %TODO find a way around using this constant

%Define
%--Generate all possible term combinations--
%Variables of inconsistent function F
variable(F,N) :- term(F,_,N), inconsistent(E,F,_).

%Total number of variables of function F
total_variables(F,T) :- T = #count{N : variable(F,N)}, inconsistent(E,F,_).

%Levels represent the number of terms held by each clause, e.g. in level 1 each clause will only have 1 term,
%in level L there will be a single clause for all L terms
level(F,1..T) :- total_variables(F,T).
 
%Calculate how many clauses exactly each level should have
level_clause_total(F,L,TOTAL) :- level(F,L), total_variables(F,T), TOTAL = @combination(T,L).

%Clauses occupied by generated terms
clause(F,L,1..CTOTAL) :- level(F,L), level_clause_total(F,L,CTOTAL).
  
%Generate terms for every clause of every level (all possible function terms are generated here)
%e.g for {a,b,c}:
%level 1 (3 clauses, 1 term each):   a; b; c
%level 2 (3 clauses, 2 terms each):  a & b; a & c ; b & c 
%level 3 (1 clause, 3 terms in it): a & b & c
%F - inconsistent function
%L - the level of the generated term
%N - the variable being placed in clause C of level L
%C - the clause of level L that is being considered
{generated_term(F,L,N,C) : variable(F,N)} = L :- clause(F,L,C).


%--Generate all possible functions--
%IDs of each candidate
id(F,1..max_candidates) :- inconsistent(_,F,_).

%Clause C1 of level L1 is not contained in clause C2 of level L2 (necessary because
%we're only interested in generating function candidates in the BCF form, which is the disjunction
%of prime implicants. If a clause C1 is contained inside of another clause C2, then C2 is not a prime implicant,
%and therefore cannot be in the same function as C1.)
not_contained_in(F,L1,C1,L2,C2) :- clause(F,L1,C1), clause(F,L2,C2), generated_term(F,L1,N,C1), not generated_term(F,L2,N,C2), L2 > L1.

%How many clauses there will be in a given candidate (used to ensure we are generating all candidates with
%1,2,...,MAX clauses possible)
function_clauses(F,1..MAX_CLAUSES) :- total_variables(F,T), MAX_CLAUSES = @combination(T,T/2).

%function_candidate(F,ID,CLAUSE_NUMBER,L,C)
%F - inconsistent function
%ID - unique ID of this function candidate
%CLAUSE_NUMBER - number of total clauses in this candidate
%L - level of the generated clause that is a part of this candidate
%C - number of the generated clause that is a part of this candidate
{function_candidate(F,ID,CLAUSE_NUMBER,L,C) : function_clauses(F, CLAUSE_NUMBER), clause(F,L,C), id(F,ID)}.

%If two distinct function candidates with the same number of clauses have at least one clause that is present in
%one candidate but not in the other, then they are distinct
distinct_candidates(F,ID1,ID2) :- function_candidate(F,ID1,CLAUSE_NUMBER,L,C), function_candidate(F,ID2,CLAUSE_NUMBER,_,_),
  not function_candidate(F,ID2,CLAUSE_NUMBER,L,C), ID1 < ID2.


%Test
%--Generate all possible term combinations--
%Clauses must be unique
:- #count{N : generated_term(F,L,N,C1), generated_term(F,L,N,C2)} = L, clause(F,L,C1), clause(F,L,C2), C2 > C1.

%Each variable occurs exactly (T-1) C (L-1) times in each level 
:- level(F,L), total_variables(F,T), variable(F,N), #count{ 1,C : generated_term(F,L,N,C)} != @combination(T-1,L-1).


%--Generate all possible functions--
%Functions must contain as many clauses as their CLAUSE_NUMBER
:- function_candidate(F,ID,CLAUSE_NUMBER,_,_), #count{1,L,C : function_candidate(F,ID,CLAUSE_NUMBER,L,C)} != CLAUSE_NUMBER.

%Clauses in a function cannot contain any other clause in that function (BCF)
:- function_candidate(F,ID,CLAUSE_NUMBER,L1,C1), function_candidate(F,ID,CLAUSE_NUMBER,L2,C2), not not_contained_in(F,L1,C1,L2,C2), L2 > L1.

%Function candidates must be distinct
:- function_candidate(F,ID1,CLAUSE_NUMBER,_,_), function_candidate(F,ID2,CLAUSE_NUMBER,_,_), ID1 < ID2, 
    not distinct_candidates(F,ID1,ID2).

%IDs must be unique
:- function_candidate(F,ID,CLAUSE_NUMBER1,_,_), function_candidate(F,ID,CLAUSE_NUMBER2,_,_), CLAUSE_NUMBER1 != CLAUSE_NUMBER2.


%Display
%#show function_clauses/2.
#show total_variables/2.
#show level_clause_total/3.
#show function_candidate/5.
%#show distinct_candidates/3.
%#show not_contained_in/5.
#show generated_term/4.


%Optimize
#maximize{1,F,ID : function_candidate(F,ID,CLAUSE_NUMBER,L,C)}.
