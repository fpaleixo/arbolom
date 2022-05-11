%Compounds
node(v1).
node(v2).
node(v3).
node(v4).

%Regulators of v1
edge(v2, v1, 0).
edge(v4, v1, 0).
edge(v3, v1, 1).

%Regulatory function of v1
function(v1, 2).
term(v1, 1, v2).
term(v1, 2, v3).
term(v1, 2, v4).

%Regulators of v2
edge(v1, v2, 0).
edge(v3, v2, 0).

%Regulatory function of v2
function(v2, 2).
term(v2, 1, v1).
term(v2, 2, v3).

%Regulators of v3
edge(v2, v3, 1).

%Regulatory function of v3
function(v3, 1).
term(v3, 1, v2).

%Regulators of v4
edge(v4, v4, 1).
edge(v3, v4, 0).

%Regulatory function of v4
function(v4, 1).
term(v4, 1, v3).
term(v4, 1, v4).

