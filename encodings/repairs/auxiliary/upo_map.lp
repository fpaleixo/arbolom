%Outputs one answer set per observation that precedes a positive observation
%(the answer set contains all compound states of the preceding observation)
#const compound = c.

%Define
%Calculate maximimum experiments and time steps
max_experiment(E) :- experiment(E), not experiment(E + 1).
max_timestep(T) :- curated_observation(_,T,_,_), not curated_observation(_,T + 1,_,_).

%Choose an experiment and time step (these must belong to some positive observation,
%as enforced by the integrity constraint below)
1{chosen_experiment(1..E) : max_experiment(E)}1.
1{chosen_timestep(1..T) : max_timestep(T)}1.

%The observations before positive observations are previous_observations
previous_observation(E,T-1,COMPOUND,S) :- curated_observation(E,T,compound,1), 
  chosen_experiment(E), chosen_timestep(T), curated_observation(E,T-1,COMPOUND,S).

%Test
%The chosen experiment and timestep must belong to some positive obesrvation
:- chosen_experiment(E), chosen_timestep(T), not curated_observation(E,T,compound,1).

#show previous_observation/4.
