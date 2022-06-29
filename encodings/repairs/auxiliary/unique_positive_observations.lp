%Identifies the unique positive observations in an LP observations
%Positive observations are observations where the compound is active
positive_observation(E,T) :- curated_observation(E,T,compound,1), T > 0.

%If we have at least some observation where the compound is active at a T > 0,
%then we have positive observations
positive_observations :- positive_observation(_,_).

%If two positive observations have at least one compound in differing states, they are not equal
unequal_positive_observations(E1,T1,E2,T2) :- positive_observation(E1,T1), positive_observation(E2,T2), 
  curated_observation(E1,T1,COMPOUND,S1), curated_observation(E2,T2,COMPOUND,S2), E2 > E1, S1 != S2, T1 > 0, T2 > 0.

unequal_positive_observations(E,T1,E,T2) :- positive_observation(E,T1), positive_observation(E,T2), 
  curated_observation(E,T1,COMPOUND,S1), curated_observation(E,T2,COMPOUND,S2), T2 > T1, S1 != S2, T1 > 0, T2 > 0.

%Two positive observations with no compounds in differing states are equal
equal_positive_observations(E1,T1,E2,T2) :- positive_observation(E1,T1), positive_observation(E2,T2), 
  not unequal_positive_observations(E1,T1,E2,T2), T1 > 0, T2 > 0, E2 > E1.
  
equal_positive_observations(E,T1,E,T2) :- positive_observation(E,T1), positive_observation(E,T2), 
  not unequal_positive_observations(E,T1,E,T2), T1 > 0, T2 > 0, T2 > T1.

%If two equal positive observations originate from previous observations that are not equal to one another, then
%explaining one observation does not ensure that we can explain the other, and as such
%we cannot consider that the positive observations are duplicated
non_duplicate_equal_observations(E1,T1,E2,T2) :- equal_positive_observations(E1,T1,E2,T2), 
  curated_observation(E1,T1-1,COMPOUND,S1), curated_observation(E2,T2-1,COMPOUND,S2), S1 != S2.

%If two equal positive observations come from previous observations that are also equal, then if we
%are able to explain one of the observations we can automatically explain the other, and thus we can say that the
%second one is duplicated
duplicate_observation(E2,T2) :- equal_positive_observations(E1,T1,E2,T2), not non_duplicate_equal_observations(E1,T1,E2,T2).

%If a positive observation has not been marked as a duplicate, then it is unique and we must
%ensure that some node covers it in some next rule
unique_positive_observation(E,T) :- positive_observation(E,T), not duplicate_observation(E,T).