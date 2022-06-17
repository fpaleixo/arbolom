%Generates the nodes containing all possible variable conjuntions

%Define
%Choose the configuration to use
{chosen_configuration(1..TCONFS)} = 1 :- total_configurations(TCONFS).

%Choose the number of variables that will be in the generated node
{node_variable_number(1..TV)} = 1 :- configuration_variable_number(CONF, TV), chosen_configuration(CONF).

%For the chosen number of variables, generate a node with that exact number of variables
{node_variable(CONF,V) : configuration_variable(CONF,V)} = VNO :- node_variable_number(VNO), chosen_configuration(CONF).


%Display
#show node_variable/2.
