% Encoding used to calculate ancestors of monotone Boolean functions

%TODO - optimize for more than 3 variables

%Define
%Variables of function F
variable(F,N) :- term(F,_,N), function(F,_).

%Total number of variables of function F
total_variables(F,T) :- T = #count{N : variable(F,N)}, function(F,_).

%Place all variables in all possible combinations
{generated_term(F,1..T,N,1..T)} :- total_variables(F,T), variable(F,N).

%Clauses occupied by generated terms
clause(F,L,C) :- generated_term(F,L,N,C).

%Total number T of terms on clause C of level L
terms_per_clause(F,L,C,T) :- T = #count{N : generated_term(F,L,N,C)}, function(F,_), clause(F,L,C).

%Count total generated terms
generated_term_count(S) :- S = #count{F,L,T,C: generated_term(F,L,T,C)}.

%We want to generate all possible terms
#maximize{S : generated_term_count(S)}.


%*
%Rule 1

%Function belonging to a node n with t+1 terms and at level 1
function(n,t+1,1) :- function(n,t).
term(n,t,r,l):- function(n,t,l), term(n,t,r).


%Rule 2


%Rule 3

*%
%Test
%Fill in clauses in order
:- clause(F,L,C+1), not clause(F,L,C), C > 0.

%Number of terms per clause must to be equal to the level
:- terms_per_clause(_,L,_,T), T != L.

%Every clause must be unique
:- clause(F,L,C1), clause(F,L,C2), C1 != C2, 
    REPETITIONS = #count{N : generated_term(F,L,N,C1), generated_term(F,L,N,C2)}, REPETITIONS = L.

#show generated_term/4.
%*
#show generated_term_count/1.
#show total_variables/2.
#show terms_per_clause/4.
*%