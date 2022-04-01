%Compounds
node(v1).
node(v2).
node(v3).

%Regulators of v2
edge(v3, v2, 1).

%Regulatory function of v2
function(v2, 1).
term(v2, 1, v3).

%Regulators of v3
edge(v1, v3, 1).
edge(v2, v3, 0).

%Regulatory function of v3
function(v3, 1).
term(v3, 1, v1).
term(v3, 1, v2).

