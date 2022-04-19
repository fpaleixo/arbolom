%Compounds
node(v1).
node(v2).
node(v3).

%Regulators of v1
edge(v2, v1, 1).

%Regulatory function of v1
function(v1, 1).
term(v1, 1, v2).

%Regulators of v2
edge(v3, v2, 1).
edge(v2, v2, 1).

%Regulatory function of v2
function(v2, 2).
term(v2, 1, v3).
term(v2, 2, v2).

