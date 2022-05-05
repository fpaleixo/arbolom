%Generates the edges between a node and its ancestors (an ancestor of node n is a node that contains all of n's variables)

%Calculate the number of variables per node
node_varno(N,N_VARNO) :- N_VARNO = #count{ V : node_variable(N,V) }, node_id(N).

%Create edges between nodes and direct ancestors (a direct ancestor has one more variable than its children)
edge(N2,N1) :- node_varno(N1,N1_VARNO), node_varno(N2,N2_VARNO), N1_VARNO = N2_VARNO + 1,
  COMMON_VARIABLES = #count{V : node_variable(N1,V), node_variable(N2,V)}, COMMON_VARIABLES = N2_VARNO.

%Create edges between nodes and all ancestors
edge(N1,N3) :- edge(N1,N2), edge(N2,N3).

#show edge/2.
