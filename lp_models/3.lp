%Compounds
node(v1).
node(v2).
node(v3).
node(v4).

%Regulators of v1
edge(v2, v1, 0).

%Regulatory function of v1
function(v1, 1).
term(v1, 1, v2).

%Regulators of v2
edge(v1, v2, 1).
edge(v4, v2, 0).

%Regulatory function of v2
function(v2, 1).
term(v2, 1, v1).
term(v2, 1, v4).

%Regulators of v3
edge(v1, v3, 0).
edge(v2, v3, 0).
edge(v4, v3, 1).

%Regulatory function of v3
function(v3, 2).
term(v3, 1, v1).
term(v3, 2, v2).
term(v3, 2, v4).

