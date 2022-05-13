%Attributes a level to every node

%Define
%Level of a node (given by the number of missing variables in that node)
node_level(N,TV - VAR_COUNT) :- node_(N), VAR_COUNT = #count{V : node_variable(N,V)}, total_variables(TV).


%Display
#show node_level/2.