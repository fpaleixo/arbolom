%Gives the level of a function

%Define
%Calculates the level of each of the function's terms (the level is the number of missing variables in the term)
func_level(T, TV - VAR_COUNT) :- VAR_COUNT = #count{V : term(F,T,V)}, term(F,T,_), total_variables(TV).

%Display
#show func_level/2.