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
node(v21).
node(v22).
node(v23).
node(v24).
node(v25).
node(v26).
node(v27).
node(v28).
node(v29).
node(v30).
node(v31).
node(v32).
node(v33).
node(v34).
node(v35).
node(v36).
node(v37).
node(v38).
node(v39).
node(v40).

%Regulators of v1
edge(v40, v1, 1).

%Regulatory function of v1
function(v1, 1).
term(v1, 1, v40).

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

%Regulators of v5
edge(v4, v5, 0).

%Regulatory function of v5
function(v5, 1).
term(v5, 1, v4).

%Regulators of v8
edge(v7, v8, 1).

%Regulatory function of v8
function(v8, 1).
term(v8, 1, v7).

%Regulators of v10
edge(v25, v10, 1).

%Regulatory function of v10
function(v10, 1).
term(v10, 1, v25).

%Regulators of v11
edge(v10, v11, 0).

%Regulatory function of v11
function(v11, 1).
term(v11, 1, v10).

%Regulators of v12
edge(v11, v12, 0).
edge(v4, v12, 0).

%Regulatory function of v12
function(v12, 2).
term(v12, 1, v11).
term(v12, 2, v4).

%Regulators of v13
edge(v12, v13, 0).

%Regulatory function of v13
function(v13, 1).
term(v13, 1, v12).

%Regulators of v15
edge(v14, v15, 0).

%Regulatory function of v15
function(v15, 1).
term(v15, 1, v14).

%Regulators of v16
edge(v15, v16, 0).
edge(v11, v16, 0).

%Regulatory function of v16
function(v16, 2).
term(v16, 1, v15).
term(v16, 2, v11).

%Regulators of v17
edge(v16, v17, 0).

%Regulatory function of v17
function(v17, 1).
term(v17, 1, v16).

%Regulators of v18
edge(v17, v18, 0).

%Regulatory function of v18
function(v18, 1).
term(v18, 1, v17).

%Regulators of v19
edge(v18, v19, 0).

%Regulatory function of v19
function(v19, 1).
term(v19, 1, v18).

%Regulators of v20
edge(v19, v20, 0).

%Regulatory function of v20
function(v20, 1).
term(v20, 1, v19).

%Regulators of v21
edge(v15, v21, 1).

%Regulatory function of v21
function(v21, 1).
term(v21, 1, v15).

%Regulators of v22
edge(v21, v22, 0).

%Regulatory function of v22
function(v22, 1).
term(v22, 1, v21).

%Regulators of v23
edge(v22, v23, 0).

%Regulatory function of v23
function(v23, 1).
term(v23, 1, v22).

%Regulators of v24
edge(v23, v24, 0).

%Regulatory function of v24
function(v24, 1).
term(v24, 1, v23).

%Regulators of v26
edge(v25, v26, 0).

%Regulatory function of v26
function(v26, 1).
term(v26, 1, v25).

%Regulators of v27
edge(v26, v27, 0).

%Regulatory function of v27
function(v27, 1).
term(v27, 1, v26).

%Regulators of v28
edge(v27, v28, 0).

%Regulatory function of v28
function(v28, 1).
term(v28, 1, v27).

%Regulators of v29
edge(v28, v29, 0).

%Regulatory function of v29
function(v29, 1).
term(v29, 1, v28).

%Regulators of v30
edge(v29, v30, 0).

%Regulatory function of v30
function(v30, 1).
term(v30, 1, v29).

%Regulators of v31
edge(v30, v31, 1).

%Regulatory function of v31
function(v31, 1).
term(v31, 1, v30).

%Regulators of v32
edge(v31, v32, 0).

%Regulatory function of v32
function(v32, 1).
term(v32, 1, v31).

%Regulators of v33
edge(v32, v33, 0).

%Regulatory function of v33
function(v33, 1).
term(v33, 1, v32).

%Regulators of v34
edge(v33, v34, 0).
edge(v13, v34, 1).

%Regulatory function of v34
function(v34, 2).
term(v34, 1, v33).
term(v34, 2, v13).

%Regulators of v35
edge(v34, v35, 0).

%Regulatory function of v35
function(v35, 1).
term(v35, 1, v34).

%Regulators of v38
edge(v37, v38, 0).

%Regulatory function of v38
function(v38, 1).
term(v38, 1, v37).

%Regulators of v39
edge(v38, v39, 1).

%Regulatory function of v39
function(v39, 1).
term(v39, 1, v38).

%Regulators of v40
edge(v39, v40, 0).

%Regulatory function of v40
function(v40, 1).
term(v40, 1, v39).

