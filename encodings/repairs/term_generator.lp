%Generates the terms to be used in creating function candidates

%Define
%Choose the function to generate terms for (only one per answer set, as enforced by the IC below)
{inconsistent_function(F)} :- inconsistent(_,F,_).

%Get the variables (regulators) of the inconsistent function
variable(F,N) :- term(F,_,N), inconsistent_function(F).

%Determine the total number of variables of the inconsistent function
total_variables(F,T) :- T = #count{N : variable(F,N)}, inconsistent_function(F).

%Choose the number of variables that will be in the generated term
{term_variable_number(F,1..T)} = 1 :- total_variables(F,T).

%For the chosen number of variables, generate a term with that exact number of variables
{generated_term(F,TN,N) : variable(F,N)} = TN :- term_variable_number(F,TN).


%Test 
%Only one function can be chosen in each answer set (to avoid duplicated generated terms, 
%e.g. generated_term(f1,1,a), generated_term(f2,1,a) in one answer set and generated_term(f1,1,a), generated_term(f2,1,b) in another)
:- #count{F : inconsistent_function(F)} != 1.


%Display
#show total_variables/2.
#show generated_term/3.

