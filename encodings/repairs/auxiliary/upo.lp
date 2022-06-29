%Identifies the unique positive observations in an LP with observations
%Positive observations are observations where the compound is active
positive_observation(E,T) :- curated_observation(E,T,compound,1), T > 0.

%If we have at least some observation where the compound is active at a T > 0,
%then we have positive observations
positive_observations :- positive_observation(_,_).

%The observations before positive observations are their causes
positive_observation_cause(E,T-1) :- positive_observation(E,T).

%Two causes with distinct compound states are unequal
unequal_causes(E1,T1,E2,T2) :- positive_observation_cause(E1,T1), positive_observation_cause(E2,T2),
  curated_observation(E1,T1,COMPOUND,S1), curated_observation(E2,T2,COMPOUND,S2), E2 > E1, S1 != S2, T1 > 0, T2 > 0.
unequal_causes(E,T1,E,T2) :- positive_observation_cause(E,T1), positive_observation_cause(E,T2),
  curated_observation(E,T1,COMPOUND,S1), curated_observation(E,T2,COMPOUND,S2), T2 > T1, T1 > 0, T2 > 0.

%If two causes are not unequal, then they describe the same model state and thus one of the positive observations is duplicated
%(explaining the first cause's positive observation will automatically explain the second's)
duplicate_observation(E2,T2+1) :- positive_observation_cause(E1,T1), positive_observation_cause(E2,T2), 
  not unequal_causes(E1,T1,E2,T2), T1 > 0, T2 > 0, E2 > E1.
duplicate_observation(E,T2+1) :- positive_observation_cause(E,T1), positive_observation_cause(E,T2), 
  not unequal_causes(E,T1,E,T2), T1 > 0, T2 > 0, T2 > T1.

%If a positive observation has not been marked as a duplicate, then it is unique and we must
%ensure that some node covers it in some next rule
unique_positive_observation(E,T) :- positive_observation(E,T), not duplicate_observation(E,T).



