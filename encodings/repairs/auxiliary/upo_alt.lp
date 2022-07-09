%Outputs 1 unique positive observation per answer set (not better)

%The observations before positive observations are previous_observations
previous_observation(E,T-1) :- curated_observation(E,T,compound,1), T > 0.

%Calculate maximimum experiments and time steps
max_experiment(E) :- experiment(E), not experiment(E + 1).
max_timestep(T) :- previous_observation(_,T), not previous_observation(_,T + 1).

%Choose the experiment and time step to check for uniqueness
1{chosen_experiment(1..E) : max_experiment(E)}1.
1{chosen_timestep(0..T) : max_timestep(T)}1.

%The chosen experiment is distinct (necessary for IC)
distinct_observation(E,T) :- chosen_experiment(E), chosen_timestep(T).

%All previous observations with at least one compound in a distinct state
%from the state in the chosen observation, are previous observations
distinct_observation(E1,T1) :- chosen_experiment(E), chosen_timestep(T),
  previous_observation(E1,T1), curated_observation(E,T,COMPOUND,S1),
  curated_observation(E1,T1,COMPOUND,S2), S1 != S2.

%The chosen experiment and timestep must belong to some previous observation
:- chosen_experiment(E), chosen_timestep(T), not previous_observation(E,T).

%If the observation is unique, it must be distinct to all observations before it
:- previous_observation(E1,T), not distinct_observation(E1,T),
  chosen_experiment(E), E > E1.

:- previous_observation(E,T1), not distinct_observation(E,T1),
  chosen_timestep(T), T > T1.

unique_positive_observation(E,T+1) :- chosen_experiment(E), chosen_timestep(T).

#show unique_positive_observation/2.
