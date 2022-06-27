%Compounds
node(v1).
node(v10).
node(v11).
node(v12).
node(v2).
node(v3).
node(v4).
node(v5).
node(v6).
node(v7).
node(v8).
node(v9).

%Regulators of v1
edge(v3, v1, 1).
edge(v4, v1, 0).
edge(v5, v1, 0).
edge(v6, v1, 0).
edge(v7, v1, 0).
edge(v8, v1, 0).
edge(v9, v1, 0).
edge(v10, v1, 0).

%Regulatory function of v1
function(v1, 1).
term(v1, 1, v10).
term(v1, 1, v3).
term(v1, 1, v4).
term(v1, 1, v5).
term(v1, 1, v6).
term(v1, 1, v7).
term(v1, 1, v8).
term(v1, 1, v9).

%Regulators of v2
edge(v5, v2, 1).
edge(v6, v2, 0).
edge(v7, v2, 1).
edge(v8, v2, 0).
edge(v9, v2, 1).
edge(v10, v2, 0).

%Regulatory function of v2
function(v2, 3).
term(v2, 1, v5).
term(v2, 1, v6).
term(v2, 2, v7).
term(v2, 2, v8).
term(v2, 3, v10).
term(v2, 3, v9).

%Regulators of v3
edge(v1, v3, 0).
edge(v2, v3, 0).
edge(v3, v3, 0).
edge(v4, v3, 0).
edge(v5, v3, 0).
edge(v6, v3, 0).
edge(v7, v3, 0).
edge(v8, v3, 0).
edge(v9, v3, 0).

%Regulatory function of v3
function(v3, 1).
term(v3, 1, v1).
term(v3, 1, v2).
term(v3, 1, v3).
term(v3, 1, v4).
term(v3, 1, v5).
term(v3, 1, v6).
term(v3, 1, v7).
term(v3, 1, v8).
term(v3, 1, v9).

%Regulators of v4
edge(v1, v4, 0).
edge(v2, v4, 0).
edge(v3, v4, 0).
edge(v4, v4, 0).
edge(v5, v4, 0).
edge(v6, v4, 0).
edge(v7, v4, 0).
edge(v8, v4, 0).
edge(v9, v4, 0).
edge(v10, v4, 0).
edge(v11, v4, 0).

%Regulatory function of v4
function(v4, 1).
term(v4, 1, v1).
term(v4, 1, v10).
term(v4, 1, v11).
term(v4, 1, v2).
term(v4, 1, v3).
term(v4, 1, v4).
term(v4, 1, v5).
term(v4, 1, v6).
term(v4, 1, v7).
term(v4, 1, v8).
term(v4, 1, v9).

%Regulators of v5
edge(v1, v5, 0).
edge(v2, v5, 0).
edge(v3, v5, 0).
edge(v4, v5, 1).
edge(v5, v5, 0).
edge(v6, v5, 1).
edge(v7, v5, 0).
edge(v8, v5, 1).


%Regulatory function of v5
function(v5, 1).
term(v5, 1, v1).
term(v5, 1, v2).
term(v5, 1, v3).
term(v5, 1, v4).
term(v5, 1, v5).
term(v5, 1, v6).
term(v5, 1, v7).
term(v5, 1, v8).