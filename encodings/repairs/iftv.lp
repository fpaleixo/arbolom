%Obtaining inconsistent functions and total variables of each

%Define
%Identify inconsistent functions
{inconsistent_function(F)} :- inconsistent(_,F,_). %Stable state inconsistent predicate has arity 3
{inconsistent_function(F)} :- inconsistent(_,_,F,_). %Time series inconsistent predicate has arity 4 (includes the time step)

%Get the variables (regulators) of the inconsistent function
variable(V) :- term(F,_,V), inconsistent_function(F).

%Determine the total number of variables of the inconsistent function
total_variables(TV) :- TV = #count{V : variable(V)}.


%Test
%Produce one answer set per inconsistent function
:- #count{F : inconsistent_function(F)} != 1.


%Display
#show inconsistent_function/1.
#show variable/1.
#show total_variables/1.