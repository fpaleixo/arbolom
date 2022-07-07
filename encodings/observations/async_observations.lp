#const e=1. %e is no. of experiments
#const t=3. %t is max time steps

%TODO - maybe add the possibility of forcing that a specific compound's function be applied? so that we can ensure that the produced
%TODO observation will test a compound we know to be inconsistent (because asynchronous mode only requires that, at each time step, one function be applied,
%TODO which means that we can generate observations where a certain compound's function is never applied)

%Generate
experiment(1..e).
time(0..t-1).
compound_state(0..1).

1 {observation(E,T,C,S) : compound_state(S)} 1 :- experiment(E), time(T), compound(C), T = 0.


%Define
observation(E,T+1,C,1) :- active(E,T+1,C), chosen_compound(E,T,C).
observation(E,T+1,C,0) :- not active(E,T+1,C), chosen_compound(E,T,C).

%Input compounds can have any value at each time step
1 {observation(E,T+1,C,S) : compound_state(S)} 1 :- experiment(E), time(T), input_compound(C).

%If the function of C is not chosen to be applied at time step T, the value carries over to the next observation
observation(E,T+1,C,S) :- observation(E,T,C,S), not chosen_compound(E,T,C), experiment(E), time(T), not input_compound(C).

%For a given compound C with I implicants, if for experiment E at time step T there exists
%some implicant I_NO which is not inactive, then C has at least one active implicant and so is active
active(E,T+1,C) :- function(C,I), not implicant_inactive(E,T,C,I_NO), experiment(E), time(T), term(C,I_NO,_).

%A compound with no regulatory function is an input compound
input_compound(C) :- compound(C), not function(C,_).

%For a given compound C with I implicants, if there exists a regulator in implicant number I_NO
%which is an inactive activator (outputs 1 when active) in an obervation E at time step T, then implicant 
%I_NO evaluates to 0 for that observation E at time step T
implicant_inactive(E,T,C,I_NO) :- function(C,I), term(C,I_NO,R), regulates(R,C,0), observation(E,T,R,0).

%For a given compound C with I implicants, if there exists a regulator in implicant number I_NO
%which is an active inhibitor (outputs 1 when inactive) in an obervation E at time step T, then implicant 
%I_NO evaluates to 0 for that observation E at time step T
implicant_inactive(E,T,C,I_NO) :- function(C,I), term(C,I_NO,R), regulates(R,C,1), observation(E,T,R,1).

%At each time step, only one function may be applied, and the compound who the function belongs to cannot be an input compound
1 {chosen_compound(E,T,C) : compound(C), not input_compound(C)} 1 :- experiment(E), time(T).


%Test
%Observations must change the state of the model (to create more interesting observations)
state_changed(E,T,T+1):- observation(E,T,C,S1), observation(E,T+1,C,S2), S1 != S2, not input_compound(C).
:- not state_changed(E,T,T+1), experiment(E), time(T).

%Display
#show observation/4.
#show experiment/1.
#show chosen_compound/3.

