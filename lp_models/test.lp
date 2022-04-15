%Compounds
node(v1).
node(v2).
node(v3).
node(v4).
node(v5).

%Regulators of v3
edge(v1, v3, 0).
edge(v2, v3, 0).
edge(v4, v3, 1).
%edge(v5, v3, 1).

%Regulatory function of v3
function(v3, 2).
term(v3, 1, v1).
term(v3, 2, v2).
term(v3, 2, v4).
%term(v3, 3, v5).
