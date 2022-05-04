node_varno(N,NVNO) :- NVNO = #count{ V : node_variable(N,V) }.

absorbs(N1,N2) :- node_id(N1), node_id(N2), N1 != N2, COMMON = #count(V : node_variable(N1,V), node_variable(N2,V)),
node_varno(N1,N1VNO), node_varno(N2,N2VNO), COMMON = NV1VNO.

#show absorbs/2.
