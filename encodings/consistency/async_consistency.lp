%Encoding to determine a model's consistency using asynchronous observations

%Define
%Time must occur in some rule head
time(T) :- observation(_,T,_,_).

%A compound with no regulatory function is an input compound (can take any value)
input_compound(C) :- compound(C), not function(C,_).

%Input compounds can take any value, 
%but that value must be the same throughout time
0 {input_active(E,C)} 1 :- experiment(E), input_compound(C).
active(E,T,C) :- time(T), input_active(E,C).


%In T = 0, if a compound has a missing observation, clingo decides if that compound
%should be active or inactive. This will be done in such a way that the 
%curated_observation that is defined for this missing observation
%leads to the least amount of inconsistencies possible 
%(this choice is required because we lack the information of T-1 that
%would enable us to know for sure if the compound is active or not)
0 {active(E,0,C)} 1 :- experiment(E), compound(C), not input_compound(C), 
  not observation(E,0,C,_).

%Input observations are converted to curated observations
curated_observation(E,T,C,S) :- observation(E,T,C,S).

%If compound C is active at time T and there is no observation for it, fill in the missing observation
curated_observation(E,T,C,1) :- active(E,T,C), not observation(E,T,C,_), time(T), experiment(E), compound(C).

%If compound C is inactive at time T and there is no observation for it, fill in the missing observation
curated_observation(E,T,C,0) :- not active(E,T,C), not observation(E,T,C,_), time(T), experiment(E), compound(C).

%For a given compound C with I implicants, if there exists a regulator in implicant number I_NO
%which is an inactive activator (outputs 1 when active) in an observation E at time T, then implicant 
%I_NO evaluates to 0 for that observation E at time T, and so is inactive at time T
implicant_inactive(E,T,C,I_NO) :- function(C,I), term(C,I_NO,R), regulates(R,C,0), curated_observation(E,T,R,0).

%For a given compound C with I implicants, if there exists a regulator in implicant number I_NO
%which is an active inhibitor (outputs 1 when inactive) in an observation E at time T, then implicant 
%I_NO evaluates to 0 for that observation E at time T, and so is inactive at time T
implicant_inactive(E,T,C,I_NO) :- function(C,I), term(C,I_NO,R), regulates(R,C,1), curated_observation(E,T,R,1).

%For a given compound C with I implicants, if for experiment E at time T there exists
%some implicant I_NO which is not inactive, then C has at least one active implicant at time T and so will be active at time T+1
active(E,T+1,C) :- function(C,I), not implicant_inactive(E,T,C,I_NO), experiment(E), term(C,I_NO,_), time(T).

%If a compound's state has been changed from time T to T+1, identify that compound
changed_compound(E,T,C) :- curated_observation(E,T,C,S1), curated_observation(E,T+1,C,S2), S1 != S2.

%If a changed compound  C is active but there is an observation stating it should be inactive, then the model is inconsistent
inconsistent(E,T,C,1) :- changed_compound(E,T-1,C), active(E,T,C), curated_observation(E,T,C,0), T > 0.

%If a changed compound C is inactive but there is an observation stating it should be active, then the model is inconsistent
inconsistent(E,T,C,0) :- changed_compound(E,T-1,C), not active(E,T,C), curated_observation(E,T,C,1), T > 0.


%Test
%Input compounds need to take values consistent with the observations
:- curated_observation(E,T,C,0), active(E,T,C), input_compound(C).
:- curated_observation(E,T,C,1), not active(E,T,C), input_compound(C).

%In asynchronous mode, only one compound state may change at each time step 
:- changed_compound(E,T,C1), changed_compound(E,T,C2), C1 != C2.


%Display
#show experiment/1.
#show curated_observation/4.
#show inconsistent/4.


%Optimize
%Optimize for the smallest number of inconsistent compounds (applicable for when we're dealing with
%incomplete observations)
#minimize{1,E,T,C : inconsistent(E,T,C,_)}.