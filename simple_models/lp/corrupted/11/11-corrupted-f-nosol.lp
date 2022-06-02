%Compounds
node(v1).
node(v2).
node(v3).
node(v4).
node(v5).
node(v6).
node(v7).

%Regulators of v1
edge(v1, v1, 1).
edge(v3, v1, 1).
edge(v7, v1, 1).
edge(v2, v1, 1).
edge(v4, v1, 1).
edge(v5, v1, 1).
edge(v6, v1, 1).

%Regulatory function of v1
function(v1, 1).
term(v1, 1, v1).
term(v1, 1, v3).
term(v1, 1, v7).
term(v1, 1, v2).
term(v1, 1, v4).
term(v1, 1, v5).
term(v1, 1, v6).

%Regulators of v2
edge(v7, v2, 0).

%Regulatory function of v2
function(v2, 1).
term(v2, 1, v7).

%Regulators of v3
edge(v6, v3, 0).

%Regulatory function of v3
function(v3, 1).
term(v3, 1, v6).

%Regulators of v4
edge(v2, v4, 0).

%Regulatory function of v4
function(v4, 1).
term(v4, 1, v2).

%Regulators of v5
edge(v4, v5, 0).

%Regulatory function of v5
function(v5, 1).
term(v5, 1, v4).

%Regulators of v6
edge(v5, v6, 0).

%Regulatory function of v6
function(v6, 1).
term(v6, 1, v5).

%Regulators of v7
edge(v3, v7, 0).

%Regulatory function of v7
function(v7, 1).
term(v7, 1, v3).

