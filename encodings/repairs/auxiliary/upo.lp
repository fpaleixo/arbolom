
%If we have at least some observation where the compound is active at a T > 0,
%then we have positive observations
positive_observations :- curated_observation(_,T,compound,1), T > 0.

%The observations before positive observations are previous_observations
previous_observation(E,T-1) :- curated_observation(E,T,compound,1), T > 0.

%Two previous_observations with distinct compound states are distinct
distinct_observations(E1,T1,E2,T2) :- previous_observation(E1,T1), previous_observation(E2,T2),
  E2 > E1, curated_observation(E1,T1,COMPOUND,S1), 
  curated_observation(E2,T2,COMPOUND,S2), S1 != S2.

distinct_observations(E,T1,E,T2) :- previous_observation(E,T1), previous_observation(E,T2),
  T2 > T1, curated_observation(E,T1,COMPOUND,S1), 
  curated_observation(E,T2,COMPOUND,S2), S1 != S2.

%If two previous_observations are not distinct, then they describe the same model state 
%and thus one of the positive observations is duplicated
%(explaining the first positive observation will automatically explain the second)
duplicate_observation(E2,T2) :- previous_observation(E1,T1), previous_observation(E2,T2), 
  not distinct_observations(E1,T1,E2,T2), E2 > E1.

duplicate_observation(E,T2) :- previous_observation(E,T1), previous_observation(E,T2), 
  not distinct_observations(E,T1,E,T2), T2 > T1.

%If a positive observation has not been marked as a duplicate, then it is unique and we must
%ensure that some node covers it
unique_positive_observation(E,T+1) :- previous_observation(E,T), not duplicate_observation(E,T).

#show unique_positive_observation/2.


