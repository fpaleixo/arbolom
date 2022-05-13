%Gives the level of a function

%Define
%Calculates the level of each of the function's terms (the level is the number of missing variables in the term)
term_level(T, TV - VAR_COUNT) :- VAR_COUNT = #count{V : term(F,T,V)}, term(F,T,_), total_variables(TV).

%Generates the level of the function (the level of a function is a tuple with as many elements as terms in the function,
%where each element represents the level of a term, and the elements are ordered in )
1 {func_level(1..TN, L) : function(F,TN)} 1 :- term_level(T,L).

%Test
%Ensures the function level is ordered in decreasing order of term levels
:- func_level(POS1, L1), func_level(POS2, L2), POS1 < POS2, L2 > L1.

%Display
#show func_level/2.