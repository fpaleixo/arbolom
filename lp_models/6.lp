%Compounds
node(v1).
node(v2).
node(v3).
node(v4).
node(v5).

%Regulators of v1
edge(v2, v1, 0).
edge(v3, v1, 1).
edge(v4, v1, 0).
edge(v5, v1, 0).

%Regulatory function of v1
function(v1, 2).
term(v1, 1, v2).
term(v1, 1, v3).
term(v1, 1, v4).
term(v1, 2, v5).

%Regulators of v2
edge(v1, v2, 1).
edge(v3, v2, 1).
edge(v4, v2, 0).
edge(v5, v2, 0).

%Regulatory function of v2
function(v2, 4).
term(v2, 1, v1).
term(v2, 2, v3).
term(v2, 3, v4).
term(v2, 4, v5).

%Regulators of v3
edge(v1, v3, 1).
edge(v2, v3, 0).
edge(v5, v3, 0).
edge(v4, v3, 0).

%Regulatory function of v3
function(v3, 3).
term(v3, 1, v1).
term(v3, 2, v2).
term(v3, 3, v4).
term(v3, 3, v5).

%Regulators of v4
edge(v2, v4, 0).
edge(v3, v4, 0).
edge(v1, v4, 0).
edge(v5, v4, 1).

%Regulatory function of v4
function(v4, 2).
term(v4, 1, v2).
term(v4, 1, v3).
term(v4, 2, v1).
term(v4, 2, v5).

%Regulators of v5
edge(v1, v5, 0).
edge(v2, v5, 0).
edge(v3, v5, 1).
edge(v4, v5, 1).

%Regulatory function of v5
function(v5, 2).
term(v5, 1, v1).
term(v5, 1, v2).
term(v5, 2, v3).
term(v5, 2, v4).

