#const e=1. %e is no. of experiments
#const t=3. %t is max time steps
%TODO print clingo errors to console

%Generate
experiment(1..e).
time(0..t-1).
node_state(0..1).

1 {observation(E,T,N,S) : node_state(S)} 1 :- experiment(E), time(T), node(N), T = 0.


%Define
observation(E,T+1,N,1) :- active(E,T+1,N).
observation(E,T+1,N,0) :- not active(E,T+1,N), experiment(E), time(T), node(N).

%For a given node N with I implicants, if for experiment E at time step T there exists
%some implicant I_NO which is not inactive, then N has at least one active implicant and so is active
active(E,T+1,N) :- function(N,I), not implicant_inactive(E,T,N,I_NO), experiment(E), time(T), term(N,I_NO,_).

%If a node has no regulatory function (input node), then it can either be inactive or active
0{active(E,T+1,N)}1 :- experiment(E), time(T), node(N), not function(N,_).

%For a given node N with I implicants, if there exists a regulator in implicant number I_NO
%which is an inactive activator (outputs 1 when active) in an obervation E at time step T, then implicant 
%I_NO evaluates to 0 for that observation E at time step T
implicant_inactive(E,T,N,I_NO) :- function(N,I), term(N,I_NO,R), edge(R,N,0), observation(E,T,R,0).

%For a given node N with I implicants, if there exists a regulator in implicant number I_NO
%which is an active inhibitor (outputs 1 when inactive) in an obervation E at time step T, then implicant 
%I_NO evaluates to 0 for that observation E at time step T
implicant_inactive(E,T,N,I_NO) :- function(N,I), term(N,I_NO,R), edge(R,N,1), observation(E,T,R,1).


%Display
#show observation/4.
#show experiment/1.
%#show implicant_inactive/4.
