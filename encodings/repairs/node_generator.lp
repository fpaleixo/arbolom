%Generates the nodes containing all possible variable conjuntions

%Choose the number of variables that will be in the generated node
{node_variable_number(1..TV)} = 1 :- total_variables(TV).

%For the chosen number of variables, generate a node with that exact number of variables
{node_variable(V) : variable(V)} = VNO :- node_variable_number(VNO).


%Display
#show node_variable/1.
