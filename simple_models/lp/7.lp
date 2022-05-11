%Compounds
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

%Regulators of v2
edge(v4, v2, 0).

%Regulatory function of v2
function(v2, 1).
term(v2, 1, v4).

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
edge(v5, v5, 0).
edge(v6, v5, 1).

%Regulatory function of v5
function(v5, 2).
term(v5, 1, v5).
term(v5, 2, v6).

%Regulators of v6
edge(v1, v6, 1).

%Regulatory function of v6
function(v6, 1).
term(v6, 1, v1).

