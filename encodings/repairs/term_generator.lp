%Generates the terms to be used in creating function candidates

%TODO - comment things
%Define
{inconsistent_function(F)} :- inconsistent(_,F,_).

variable(F,N) :- term(F,_,N), inconsistent_function(F).

total_variables(F,T) :- T = #count{N : variable(F,N)}, inconsistent_function(F).

1{term_number(F,1..T)}1 :- total_variables(F,T).

{generated_term(F,TN,N) : variable(F,N)} = TN :- term_number(F,TN).


%Test 
:- #count{F : inconsistent_function(F)} != 1.

#show generated_term/3.

