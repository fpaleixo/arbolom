% Encoding used to calculate ancestors of monotone Boolean functions

%TODO - implement rules 2,3

%Define
%--Generate all possible term combinations--
%Factorial functions - used to determine number of terms to generate
factorial(0,1). 
factorial(N+1, F*(N+1)) :- factorial(N,F), N < TARGET, get_factorial(TARGET). 

%Variables of function F
variable(F,N) :- term(F,_,N), function(F,_).

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
  
%Generate terms for every clause of every level
{generated_term(F,L,N,1..C) : variable(F,N)} = C*L :-  level(F,L), level_clause_total(F,L,C).

%Clauses occupied by generated terms
clause(F,L,C) :- generated_term(F,L,N,C).

%Total number T of terms on clause C of level L -- this is probably very inefficient, since generated_term comes from a choice rule...
terms_per_clause(F,L,C,T) :- T = #count{N : generated_term(F,L,N,C)}, function(F,_), clause(F,L,C).


%--Rule 1--
%If for a clause C1 of the original function there is no compound N which exists in a generated clause C2, then
%the generated clause C2 does not contain the original clause C1
original_not_absorbed(F,C1,L,C2) :- term(F,C1,N), not generated_term(F,L,N,C2), clause(F,L,C2).

%If for a generated clause C2 there is no compound N in a clause C1 of the original function, then the original
%clause C1 does not contain the generated clause C2
generated_not_absorbed(F,C1,L,C2) :- generated_term(F,L,N,C2), not term(F,C1,N), term(_,C1,_).

%Labelling generated clauses C2 that contain or are contained by an existing clause C1
contained_or_contains(F,L,C2):- clause(F,L,C2), term(F,C1,_), not generated_not_absorbed(F,C1,L,C2).
contained_or_contains(F,L,C2):- clause(F,L,C2), term(F,C1,_), not original_not_absorbed(F,C1,L,C2).

%Chosen clauses by Rule 1 cannot contain any or be contained by any original clause, and need to be as large as possible
%(i.e. there cannot be chosen clauses of a higher level)
rule1_clause(F,L,C2) :- clause(F,L,C2), not contained_or_contains(F,L,C2), not rule1_clause(F,L+1,_).

%--Rule 2--


%--Rule 3--



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
%#show original_not_absorbed/4.
%#show generated_not_absorbed/4.
#show rule1_clause/3.
#show generated_term/4.
%#show generated_term_count/1.
%#show total_variables/2.
%#show terms_per_clause/4.
