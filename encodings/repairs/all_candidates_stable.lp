%Repair strategy: For each inconsistent node, generate all possible function candidates.
%Reject candidates which are not able to replicate expected behavior.

%Define
%--Generate all possible term combinations--
%Factorial functions - used to determine number of terms to generate
factorial(0,1). 
factorial(N+1, F*(N+1)) :- factorial(N,F), N < TARGET, get_factorial(TARGET). 

%Variables of inconsistent function F (function change will only work with these variables)
variable(F,N) :- term(F,_,N), inconsistent(E,F,_).

%Total number of variables of function F
total_variables(F,T) :- T = #count{N : variable(F,N)}, function(F,_).

%Levels represent the number of terms held by each clause, e.g. in level 1 each clause will only have 1 term,
%in level L there will be a single clause for all L terms
level(F,1..T) :- total_variables(F,T).

%Calculate maximum factorial required for our calculations
get_factorial(T) :- total_variables(F,T).
 
%Calculate how many clauses exactly each level should have
level_clause_total(F,L,FACT1/FACT2/FACT3) :- level(F,L), total_variables(F,T), 
    factorial(T, FACT1), factorial(T-L, FACT2), factorial(L, FACT3).
  
%Generate terms for every clause of every level (all possible function terms are generated here)
%e.g for {a,b,c}:
%level 1 (3 clauses, 1 term each):   a; b; c
%level 2 (3 clauses, 2 terms each):  a & b; a &c ; b & c 
%level 3 (1 clause, 3 terms in it): a & b & c
%F - function that could be defined by these variable combinations
%L - the level of the generated term
%N - the variable being placed in clause C of level L
%C - the clause of level L that is being considered
{generated_term(F,L,N,1..C) : variable(F,N)} = C*L :-  level(F,L), level_clause_total(F,L,C).

%Clauses occupied by generated terms
clause(F,L,C) :- generated_term(F,L,N,C).

%Total number T of terms on clause C of level L -- this is probably very inefficient, since generated_term comes from a choice rule...
terms_per_clause(F,L,C,T) :- T = #count{N : generated_term(F,L,N,C)}, function(F,_), clause(F,L,C).

%Clause C1 of level L1 is not contained in clause C2 of level L2 (necessary because
%we're only interested in generating function candidates in the BCF form, which is the disjunction
%of prime implicants. If a clause C1 is contained inside of another clause C2, then C2 is not a prime implicant,
%and therefore cannot be in the same function as C1.)
not_contained_in(F,L1,C1,L2,C2) :- clause(F,L1,C1), clause(F,L2,C2), generated_term(F,L1,N,C1), not generated_term(F,L2,N,C2), L2 > L1.


function_candidate(F,T,0) :- inconsistent(E,F,_)

:- clause(F,L1,C1), clause(F,L2,C2), not_contained_in(F,L1,C1,L2,C2).

%Test
%--Generate all possible term combinations--
%Fill in clauses in order
:- clause(F,L,C+1), not clause(F,L,C), C > 0.

%Number of terms per clause must to be equal to the level
:- terms_per_clause(_,L,_,T), T != L.

%Every clause must be unique
:- clause(F,L,C1), clause(F,L,C2), C1 != C2, 
    REPETITIONS = #count{N : generated_term(F,L,N,C1), generated_term(F,L,N,C2)}, REPETITIONS = L.


%Display
#show not_contained_in/5.
#show generated_term/4.

%Scratch
%If reported inconsistent value was 0 but should have been 1 for experiment E, then N
%needs to be changed to a more general function
%generalize(E,N) :- inconsistent(E,N,0).

%If reported inconsistent value was 1 but should have been 0 for experiment E, then N
%needs to be changed to a more specific function
%specify(E,N) :- inconsistent(E,N,1).

%If reported inconsistent value was 1 for some experiment(s) and 0 for other(s), then N
%needs to be changed to a function that isn't more general or more specific
%sidestep(N) :- generalize(_,N), specify(_,N).