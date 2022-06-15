%Creates nodes and generates the edges between a node and its ancestors (an ancestor of node n is a node that contains all of n's variables)

%Define
%--Nodes
%Define the total number of nodes
total_nodes(TN) :- total_variables(TV), TN = @calculateTotalNodes(TV).

%Define the IDs of each node
node_(1..TN) :- total_nodes(TN).

%Generate the variables in each node
1 {node_variable(N,V) : variable(V)} :- node_(N).

%Calculate the number of variables per node
node_varno(N,N_VARNO) :- N_VARNO = #count{ V : node_variable(N,V) }, node_(N).

%Create edges between nodes contained in other nodes
edge_(N1,N2) :- node_(N1), node_(N2), N1 != N2, COMMON = #count{V : node_variable(N1,V), node_variable(N2,V)},
  node_varno(N1,N1_VARNO), COMMON = N1_VARNO.


%Test
%--Nodes
%There can be no two equal nodes
:- edge_(N1,N2), edge_(N2,N1).


%Display
#show node_/1.
#show node_variable/2.


%* older version
%Creates nodes and generates the edges between a node and its ancestors (an ancestor of node n is a node that contains all of n's variables)

%Define
%--Nodes
%Define the total number of nodes
total_nodes(TN) :- total_variables(TV), TN = @calculateTotalNodes(TV).

%Define the IDs of each node
node_(1..TN) :- total_nodes(TN).

%Generate the variables in each node
1 {node_variable(N,V) : variable(V)} :- node_(N).

%If a variable is present in one node but not in another, then the two nodes are distinct
distinct_nodes(N1,N2) :- node_(N1), node_(N2), node_variable(N1,V), not node_variable(N2,V), N1 < N2.
%Symmetry breaking
distinct_nodes(N1,N2) :- node_(N1), node_(N2), not node_variable(N1,V), node_variable(N2,V), N1 < N2.

%--Edges
%Calculate the number of variables per node
node_varno(N,N_VARNO) :- N_VARNO = #count{ V : node_variable(N,V) }, node_(N).

%Create edges between nodes and direct ancestors (a direct ancestor has one more variable than its children)
edge_(N2,N1) :- node_varno(N1,N1_VARNO), node_varno(N2,N2_VARNO), N1_VARNO = N2_VARNO + 1,
  COMMON_VARIABLES = #count{V : node_variable(N1,V), node_variable(N2,V)}, COMMON_VARIABLES = N2_VARNO.

%Create edges between nodes and all ancestors
edge_(N1,N3) :- edge_(N1,N2), edge_(N2,N3).

%Test
%--Nodes
%There can be no two equal nodes
:- node_(N1), node_(N2), N1 < N2, not distinct_nodes(N1,N2).



%Display
#show node_/1.
#show node_variable/2.
*/