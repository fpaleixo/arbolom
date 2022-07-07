#const e=1. %e is no. of experiments
#const t=3. %t is max time steps


%Generate
experiment(1..e).
time(0..t-1).
compound_state(0..1).

1 {observation(E,T,C,S) : compound_state(S)} 1 :- experiment(E), time(T), compound(C), T = 0.


%Define
observation(E,T+1,C,1) :- active(E,T+1,C).
observation(E,T+1,C,0) :- not active(E,T+1,C), experiment(E), time(T), compound(C).

%For a given compound C with I implicants, if for experiment E at time step T there exists
%some implicant I_NO which is not inactive, then C has at least one active implicant and so is active
active(E,T+1,C) :- function(C,I), not implicant_inactive(E,T,C,I_NO), experiment(E), time(T), term(C,I_NO,_).

%If a compound has no regulatory function (input compound), then it can either be inactive or active
0{active(E,T+1,C)}1 :- experiment(E), time(T), compound(C), not function(C,_).

%For a given compound C with I implicants, if there exists a regulator in implicant number I_NO
%which is an inactive activator (outputs 1 when active) in an obervation E at time step T, then implicant 
%I_NO evaluates to 0 for that observation E at time step T
implicant_inactive(E,T,C,I_NO) :- function(C,I), term(C,I_NO,R), regulates(R,C,0), observation(E,T,R,0).

%For a given compound C with I implicants, if there exists a regulator in implicant number I_NO
%which is an active inhibitor (outputs 1 when inactive) in an obervation E at time step T, then implicant 
%I_NO evaluates to 0 for that observation E at time step T
implicant_inactive(E,T,C,I_NO) :- function(C,I), term(C,I_NO,R), regulates(R,C,1), observation(E,T,R,1).


%Display
#show observation/4.
#show experiment/1.
