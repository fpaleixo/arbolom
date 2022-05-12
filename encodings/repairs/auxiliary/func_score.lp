%Gives a score to a monotone, non-degenerate Boolean function in the DNF (written in the standard format).

%Define
%Number of disjunctions
or_score(OS) :- function(V,OS).

%Number of conjunctions (or_score is subtracted from VAR_COUNT because simply summing up all variables would lead to
%counting an extra or_score conjunctions that do not exist, so they must be subtracted)
and_score(AS) :- VAR_COUNT = #count{V,T,R : term(V,T,R)}, AS = VAR_COUNT - OS, or_score(OS).

%Final score is given by the total number of conjunctions - disjunctions
func_score(AS - OS) :- or_score(OS), and_score(AS).


%Display
#show func_score/1.