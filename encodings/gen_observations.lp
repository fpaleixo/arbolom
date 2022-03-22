#const e=1. %e is no. of experiments
#const t=3. %t is max time steps

%Base
exp(1..e).
time(0..t-1).
state(0..1).

%Step
obs_exp(W,X,Y,Z):- exp(W),time(X),node(Y),state(Z).


