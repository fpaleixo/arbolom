#const compound = c.

%Calculate maximimum experiments and time steps
max_experiment(E) :- experiment(E), not experiment(E + 1).
max_timestep(T) :- curated_observation(_,T,_,_), not curated_observation(_,T + 1,_,_).

%Choose the experiment and time step to check for uniqueness
1{chosen_experiment(1..E) : max_experiment(E)}1.
1{chosen_timestep(0..T) : max_timestep(T)}1.

%The observations before positive observations are previous_observations
previous_observation(E,T-1) :- curated_observation(E,T,compound,1), T > 0, 
  chosen_experiment(E), chosen_timestep(T-1).

previous_state(E,T,COMPOUND,S) :- curated_observation(E,T,COMPOUND,S), previous_observation(E,T).

:- 0{previous_observation(E,T)}0.

#show previous_state/4.
