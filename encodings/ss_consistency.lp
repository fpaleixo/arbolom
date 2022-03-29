%There can be no inconsistent nodes
:- inconsistent(E,N), node(N), experiment(E).

%If node  N is active but there is an observation stating it should be inactive, then the model is inconsistent
inconsistent(E,N) :- active(E,N), not input_node(N), observation(E,N,0).

%If compound N is inactive but there is an observation stating it should be active, then the model is inconsistent
inconsistent(E,N) :- not active(E,N), not input_node(N), observation(E,N,1).

%A node with no regulatory function is an input node (can take any value)
input_node(N) :- node(N), not function(N,_).

%For a given node N with I implicants, if for experiment E there exists
%some implicant I_NO which is not inactive, then N has at least one active implicant and so is active
active(E,N) :- function(N,I), not implicant_inactive(E,N,I_NO), experiment(E), term(N,I_NO,_).

%For a given node N with I implicants, if there exists a regulator in implicant number I_NO
%which is an inactive activator (outputs 1 when active) in an obervation E, then implicant 
%I_NO evaluates to 0 for that observation E, and so is inactive
implicant_inactive(E,N,I_NO) :- function(N,I), term(N,I_NO,R), edge(R,N,0), observation(E,R,0).

%For a given node N with I implicants, if there exists a regulator in implicant number I_NO
%which is an active inhibitor (outputs 1 when inactive) in an obervation E at time step T, then implicant 
%I_NO evaluates to 0 for that observation E, and so is inactive
implicant_inactive(E,N,I_NO) :- function(N,I), term(N,I_NO,R), edge(R,N,1), observation(E,R,1).

#show inconsistent/2.
#show node/1.
