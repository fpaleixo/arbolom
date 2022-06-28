%Compounds
node(v1).
node(v10).
node(v11).
node(v12).
node(v13).
node(v14).
node(v15).
node(v16).
node(v17).
node(v18).
node(v19).
node(v2).
node(v20).
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

%Regulators of v6
edge(v1, v6, 1).
edge(v2, v6, 1).
edge(v3, v6, 1).
edge(v4, v6, 1).
edge(v5, v6, 1).
edge(v6, v6, 1).
edge(v7, v6, 1).
edge(v8, v6, 1).

%Regulatory function of v6
function(v6, 3).
term(v6, 1, v1).
term(v6, 1, v2).
term(v6, 1, v3).
term(v6, 2, v4).
term(v6, 2, v5).
term(v6, 3, v6).
term(v6, 3, v7).
term(v6, 3, v8).

%Regulators of v7
edge(v1, v7, 1).
edge(v2, v7, 1).
edge(v3, v7, 1).
edge(v16, v7, 1).
edge(v4, v7, 1).
edge(v5, v7, 1).
edge(v17, v7, 1).
edge(v6, v7, 1).
edge(v8, v7, 1).
edge(v18, v7, 1).
edge(v10, v7, 1).
edge(v11, v7, 1).
edge(v19, v7, 1).

%Regulatory function of v7
function(v7, 4).
term(v7, 1, v1).
term(v7, 1, v16).
term(v7, 1, v2).
term(v7, 1, v3).
term(v7, 2, v17).
term(v7, 2, v4).
term(v7, 2, v5).
term(v7, 3, v18).
term(v7, 3, v6).
term(v7, 3, v8).
term(v7, 4, v10).
term(v7, 4, v11).
term(v7, 4, v19).

%Regulators of v8
edge(v2, v8, 0).

%Regulatory function of v8
function(v8, 1).
term(v8, 1, v2).

%Regulators of v9
edge(v3, v9, 0).

%Regulatory function of v9
function(v9, 1).
term(v9, 1, v3).

%Regulators of v10
edge(v4, v10, 0).

%Regulatory function of v10
function(v10, 1).
term(v10, 1, v4).

%Regulators of v11
edge(v5, v11, 0).

%Regulatory function of v11
function(v11, 1).
term(v11, 1, v5).

%Regulators of v12
edge(v6, v12, 0).

%Regulatory function of v12
function(v12, 1).
term(v12, 1, v6).

%Regulators of v13
edge(v7, v13, 0).

%Regulatory function of v13
function(v13, 1).
term(v13, 1, v7).

%Regulators of v14
edge(v8, v14, 0).

%Regulatory function of v14
function(v14, 1).
term(v14, 1, v8).

%Regulators of v15
edge(v9, v15, 0).

%Regulatory function of v15
function(v15, 1).
term(v15, 1, v9).

%Regulators of v16
edge(v10, v16, 0).

%Regulatory function of v16
function(v16, 1).
term(v16, 1, v10).

%Regulators of v17
edge(v11, v17, 0).

%Regulatory function of v17
function(v17, 1).
term(v17, 1, v11).

%Regulators of v18
edge(v12, v18, 0).

%Regulatory function of v18
function(v18, 1).
term(v18, 1, v12).

%Regulators of v19
edge(v13, v19, 0).

%Regulatory function of v19
function(v19, 1).
term(v19, 1, v13).

