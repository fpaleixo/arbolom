%Encoding to determine a model's consistency using stable state observations

%Define
%A compound with no regulatory function is an input compound
input_compound(C) :- compound(C), not function(C,_).

%Input compounds can take any value
0 {active(E,C)} 1 :- experiment(E), input_compound(C).

%Input observations are converted to curated observations
curated_observation(E,C,S) :- observation(E,C,S).

%If compound C has no observation for it, fill in the missing observation
1 {curated_observation(E,C,0); curated_observation(E,C,1)} 1 :- not observation(E,C,_), experiment(E), compound(C).

%For a given compound C with I implicants, if there exists a regulator in implicant number I_NO
%which is an inactive activator (outputs 1 when active) in an obervation E, then implicant 
%I_NO evaluates to 0 for that observation E, and so is inactive
implicant_inactive(E,C,I_NO) :- function(C,I), term(C,I_NO,R), regulates(R,C,0), curated_observation(E,R,0).

%For a given compound C with I implicants, if there exists a regulator in implicant number I_NO
%which is an active inhibitor (outputs 1 when inactive) in an obervation E at time step T, then implicant 
%I_NO evaluates to 0 for that observation E, and so is inactive
implicant_inactive(E,C,I_NO) :- function(C,I), term(C,I_NO,R), regulates(R,C,1), curated_observation(E,R,1).

%For a given compound C with I implicants, if for experiment E there exists
%some implicant which is not inactive, then C has at least one active implicant and so is active
active(E,C) :- function(C,I), not implicant_inactive(E,C,I_NO), experiment(E), term(C,I_NO,_).

%If compound  C is active but there is an observation stating it should be inactive, then the model is inconsistent
inconsistent(E,C,1) :- active(E,C), curated_observation(E,C,0).

%If compound C is inactive but there is an observation stating it should be active, then the model is inconsistent
inconsistent(E,C,0) :- not active(E,C), curated_observation(E,C,1).


%Test
%Input compounds need to take values consistent with the observations
:- curated_observation(E,C,0), active(E,C), input_compound(C).
:- curated_observation(E,C,1), not active(E,C), input_compound(C).


%Display
#show experiment/1.
#show inconsistent/3.
#show curated_observation/3.


%Optimize
%Optimize for the smallest number of inconsistent compounds (applicable for when we're dealing with
%incomplete observations)
#minimize{1,E,C : inconsistent(E,C,_)}.