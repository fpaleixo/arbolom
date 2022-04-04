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
node(v20).

%Regulators of v1
edge(v20, v1, 0).

%Regulatory function of v1
function(v1, 1).
term(v1, 1, v20).

%Regulators of v2
edge(v1, v2, 0).

%Regulatory function of v2
function(v2, 1).
term(v2, 1, v1).

%Regulators of v3
edge(v2, v3, 0).

%Regulatory function of v3
function(v3, 1).
term(v3, 1, v2).

%Regulators of v4
edge(v3, v4, 0).

%Regulatory function of v4
function(v4, 1).
term(v4, 1, v3).

%Regulators of v6
edge(v5, v6, 0).

%Regulatory function of v6
function(v6, 1).
term(v6, 1, v5).

%Regulators of v7
edge(v6, v7, 0).

%Regulatory function of v7
function(v7, 1).
term(v7, 1, v6).

%Regulators of v8
edge(v7, v8, 0).

%Regulatory function of v8
function(v8, 1).
term(v8, 1, v7).

%Regulators of v10
edge(v9, v10, 0).

%Regulatory function of v10
function(v10, 1).
term(v10, 1, v9).

%Regulators of v11
edge(v10, v11, 1).

%Regulatory function of v11
function(v11, 1).
term(v11, 1, v10).

%Regulators of v12
edge(v11, v12, 0).

%Regulatory function of v12
function(v12, 1).
term(v12, 1, v11).

%Regulators of v13
edge(v12, v13, 0).

%Regulatory function of v13
function(v13, 1).
term(v13, 1, v12).

%Regulators of v14
edge(v13, v14, 0).

%Regulatory function of v14
function(v14, 1).
term(v14, 1, v13).

%Regulators of v15
edge(v14, v15, 0).

%Regulatory function of v15
function(v15, 1).
term(v15, 1, v14).

%Regulators of v16
edge(v15, v16, 0).

%Regulatory function of v16
function(v16, 1).
term(v16, 1, v15).

%Regulators of v18
edge(v17, v18, 0).

%Regulatory function of v18
function(v18, 1).
term(v18, 1, v17).

