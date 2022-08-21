#const e=1. %e is no. of experiments
#const t=3. %t is max time steps

%Define
experiment(1..e).
time(0..t).
compound_state(0..1).

%If a compound C has a single term, with a single regulator in that term, 
%and it has itself as an activator, then C is an input compound
input_compound(C) :- compound(C), function(C,1), regulates(C,C,0), #count{R : term(C,1,R)} = 1.

%Input compounds can take any value, 
%but that value must be the same throughout time
0 {input_active(E,C)} 1 :- experiment(E), input_compound(C).
active(E,T,C) :- time(T), input_active(E,C).

%Choose initial state for non-input compounds
0 {active(E,0,C)} 1 :- experiment(E), compound(C), not input_compound(C).

%For a given compound C with I implicants, if there exists a regulator in implicant number I_NO
%which is an inactive activator (outputs 1 when active) in an obervation E at time step T, then implicant 
%I_NO evaluates to 0 for that observation E at time step T
implicant_inactive(E,T,C,I_NO) :- function(C,I), term(C,I_NO,R), regulates(R,C,0), observation(E,T,R,0).

%For a given compound C with I implicants, if there exists a regulator in implicant number I_NO
%which is an active inhibitor (outputs 1 when inactive) in an obervation E at time step T, then implicant 
%I_NO evaluates to 0 for that observation E at time step T
implicant_inactive(E,T,C,I_NO) :- function(C,I), term(C,I_NO,R), regulates(R,C,1), observation(E,T,R,1).

%For a given compound C with I implicants, if for experiment E at time step T there exists
%some implicant I_NO which is not inactive, then C has at least one active implicant and so is active
active(E,T,C) :- function(C,I), not implicant_inactive(E,T-1,C,I_NO), experiment(E), time(T), term(C,I_NO,_), T > 0.

%If a compound is active at a given timestep, then it produces a positive
%observation
observation(E,T,C,1) :- active(E,T,C).

%If a compound is inactive at a given timestep, then it produces a negative
%observation
observation(E,T,C,0) :- not active(E,T,C), experiment(E), time(T), compound(C).

%If two experiments E1, E2 display different states S1,S2 for the same compound C at the
%same time step T, then they are distinct
distinct_experiments(E1,E2) :- observation(E1,T,C,S1), observation(E2,T,C,S2), E2 > E1, S1 != S2.


%Display
#show observation/4.
#show experiment/1.


%Optimize
%Whenever possible, it is desirable that the generated experiments are distinct
#maximize{1,E1,E2 : distinct_experiments(E1,E2)}.
