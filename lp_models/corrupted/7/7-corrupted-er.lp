%Compounds
node().
node(v1).
node(v2).
node(v3).
node(v4).
node(v5).
node(v6).

%Regulators of v1
edge(v2, v1, 1).
edge(v3, v1, 0).

%Regulatory function of v1
function(v1, 1).
term(v1, 1, v2).
term(v1, 1, v3).

%Regulators of v3
edge(v5, v3, 1).
edge(v6, v3, 1).

%Regulatory function of v3
function(v3, 2).
term(v3, 1, v5).
term(v3, 2, v6).

%Regulators of v4
edge(v5, v4, 1).

%Regulatory function of v4
function(v4, 1).
term(v4, 1, v5).

%Regulators of v5
edge(v6, v5, 1).

%Regulatory function of v5
function(v5, 1).
term(v5, 1, v6).

