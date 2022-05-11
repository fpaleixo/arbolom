%Compounds
node(v1).
node(v2).
node(v3).
node(v4).
node(v5).
node(v6).
node(v7).
node(v8).
node(v9).

%Regulators of v1
edge(v2, v1, 1).
edge(v3, v1, 0).
edge(v4, v1, 1).
edge(v5, v1, 1).
edge(v6, v1, 1).

%Regulatory function of v1
function(v1, 4).
term(v1, 1, v2).
term(v1, 1, v3).
term(v1, 2, v3).
term(v1, 2, v4).
term(v1, 3, v3).
term(v1, 3, v5).
term(v1, 4, v3).
term(v1, 4, v6).

%Regulators of v2
edge(v7, v2, 1).

%Regulatory function of v2
function(v2, 1).
term(v2, 1, v7).

%Regulators of v3
edge(v8, v3, 1).

%Regulatory function of v3
function(v3, 1).
term(v3, 1, v8).

%Regulators of v4
edge(v9, v4, 1).

%Regulatory function of v4
function(v4, 1).
term(v4, 1, v9).

%Regulators of v8
edge(v8, v8, 1).
edge(v6, v8, 1).

%Regulatory function of v8
function(v8, 1).
term(v8, 1, v6).
term(v8, 1, v8).

%Regulators of v9
edge(v9, v9, 1).
edge(v5, v9, 0).

%Regulatory function of v9
function(v9, 1).
term(v9, 1, v5).
term(v9, 1, v9).

