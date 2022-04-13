%Encoding used to calculate ancestors of monotone Boolean functions

%Define
%Variables of function F
variable(F,N) :- term(F,_,N), function(F,_).

%Total number of variables of function F
total_variables(F,T) :- T = #count{variable(F,N): term(F,_,N)}, function(F,_).

%Generate levels and clauses
level(F,1..T) :- total_variables(F,T).
clause(F,L,1..T) :- total_variables(F,T), level(F,L).

%At the maximum level (T) of generated terms, all variables will belong to a single clause  
generated_term(F,T,N,1) :- total_variables(F,T), variable(F,N).

%At the first level of generated terms, compounds will occupy clauses from 1 to T 
1{generated_term(F,1,N,1..T)}1 :- total_variables(F,T), variable(F,N).

%At level n, clauses can have up to n variables 
{generated_term(F,2..T-1,N,1..T)} :- total_compounds(F,T), variable(F,N).

%*
%Rule 1

%Function belonging to a node n with t+1 terms and at level 1
function(n,t+1,1) :- function(n,t).
term(n,t,r,l):- function(n,t,l), term(n,t,r).


%Rule 2


%Rule 3

*%
%Test
%In the first level of generated terms, a clause C can only be occupied by one and only one term
:- generated_term(F,1,N1,C), generated_term(F,1,N2,C), N1 != N2.

test(O) :- #count{N,C : generated_term(F,L,N,C)} = O, level(F,L), function(F,_).

#show variable/2.
#show total_variables/2.
#show generated_term/4.
#show test/1.