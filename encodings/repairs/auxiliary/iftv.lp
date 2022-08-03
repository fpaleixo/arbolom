%Obtaining inconsistent functions

%Define
%Identify inconsistent functions
{inconsistent_function(F)} :- inconsistent(_,F,_). %Stable state inconsistent predicate has arity 3
{inconsistent_function(F)} :- inconsistent(_,_,F,_). %Time series inconsistent predicate has arity 4 (includes the time step)

%Test
%Produce one answer set per inconsistent function
:- #count{F : inconsistent_function(F)} != 1.

%Display
#show inconsistent_function/1.
