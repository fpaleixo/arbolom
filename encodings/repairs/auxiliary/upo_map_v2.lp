%Outputs one answer set per observation that precedes a positive observation
%(the answer set contains all compound states of the preceding observation)
#const compound = c.

%Define
previous_observation(E,T-1,C,S) :- curated_observation(E,T-1,C,S), 
  curated_observation(E,T,compound,1), T > 0.

%Display
#show previous_observation/4.
