%Compounds
node(cdc20).
node(cyca).
node(cycb).
node(cycd).
node(cyce).
node(e2f).
node(rb).
node(ubch10).
node(cdh1).
node(p27).

%Regulators of cdc20
edge(cycb, cdc20, 1).

%Regulatory function of cdc20
function(cdc20, 1).
term(cdc20, 1, cycb).

%Regulators of cyca
edge(cdc20, cyca, 1).
edge(ubch10, cyca, 1).
edge(p27, cyca, 1).
edge(cycb, cyca, 1).
edge(cyca, cyca, 1).
edge(e2f, cyca, 1).

%Regulatory function of cyca
function(cyca, 5).
term(cyca, 1, cdc20).
term(cyca, 1, ubch10).
term(cyca, 2, cdh1).
term(cyca, 2, p27).
term(cyca, 3, cyca).
term(cyca, 3, p27).
term(cyca, 4, e2f).
term(cyca, 4, p27).
term(cyca, 5, cdh1).
term(cyca, 5, cyca).

%Regulators of cycb
edge(cdc20, cycb, 0).
edge(cdh1, cycb, 0).

%Regulatory function of cycb
function(cycb, 1).
term(cycb, 1, cdc20).
term(cycb, 1, cdh1).

%Regulators of cycd
edge(cycd, cycd, 1).

%Regulatory function of cycd
function(cycd, 1).
term(cycd, 1, cycd).

%Regulators of cyce
edge(rb, cyce, 0).
edge(e2f, cyce, 1).

%Regulatory function of cyce
function(cyce, 1).
term(cyce, 1, e2f).
term(cyce, 1, rb).

%Regulators of e2f
edge(rb, e2f, 0).
edge(cyca, e2f, 0).
edge(cycb, e2f, 0).
edge(p27, e2f, 1).

%Regulatory function of e2f
function(e2f, 2).
term(e2f, 1, cyca).
term(e2f, 1, cycb).
term(e2f, 1, rb).
term(e2f, 2, cycb).
term(e2f, 2, p27).
term(e2f, 2, rb).

%Regulators of rb
edge(cycd, rb, 0).
edge(cyce, rb, 0).
edge(cyca, rb, 0).
edge(cycb, rb, 0).
edge(p27, rb, 1).

%Regulatory function of rb
function(rb, 2).
term(rb, 1, cyca).
term(rb, 1, cycb).
term(rb, 1, cycd).
term(rb, 1, cyce).
term(rb, 2, cycb).
term(rb, 2, cycd).
term(rb, 2, p27).

%Regulators of ubch10
edge(cdc20, ubch10, 1).
edge(ubch10, ubch10, 1).
edge(cycb, ubch10, 1).
edge(cyca, ubch10, 1).
edge(cdh1, ubch10, 0).

%Regulatory function of ubch10
function(ubch10, 4).
term(ubch10, 1, cdc20).
term(ubch10, 1, ubch10).
term(ubch10, 2, cycb).
term(ubch10, 2, ubch10).
term(ubch10, 3, cyca).
term(ubch10, 3, ubch10).
term(ubch10, 4, cdh1).
term(ubch10, 4, ubch10).

%Regulators of cdh1
edge(cyca, cdh1, 0).
edge(cycb, cdh1, 0).
edge(p27, cdh1, 1).
edge(cdc20, cdh1, 1).

%Regulatory function of cdh1
function(cdh1, 3).
term(cdh1, 1, cyca).
term(cdh1, 1, cycb).
term(cdh1, 2, cycb).
term(cdh1, 2, p27).
term(cdh1, 3, cdc20).

%Regulators of p27
edge(cycd, p27, 0).
edge(cyce, p27, 0).
edge(cyca, p27, 0).
edge(cycb, p27, 0).
edge(p27, p27, 1).

%Regulatory function of p27
function(p27, 3).
term(p27, 1, cyca).
term(p27, 1, cycb).
term(p27, 1, cycd).
term(p27, 1, cyce).
term(p27, 2, cyca).
term(p27, 2, cycb).
term(p27, 2, cycd).
term(p27, 2, p27).
term(p27, 3, cycb).
term(p27, 3, cycd).
term(p27, 3, cyce).
term(p27, 3, p27).

