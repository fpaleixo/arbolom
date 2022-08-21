%Compounds
compound(cdc20).
compound(cyca).
compound(cycb).
compound(cycd).
compound(cyce).
compound(e2f).
compound(rb).
compound(ubch10).
compound(cdh1).
compound(p27).

%Regulators of cdc20
regulates(cycb, cdc20, 0).

%Regulatory function of cdc20
function(cdc20, 1).
term(cdc20, 1, cycb).

%Regulators of cyca
regulates(rb, cyca, 1).
regulates(cyca, cyca, 0).
regulates(cdc20, cyca, 1).
regulates(cdh1, cyca, 1).
regulates(ubch10, cyca, 1).
regulates(e2f, cyca, 0).

%Regulatory function of cyca
function(cyca, 4).
term(cyca, 1, cdc20).
term(cyca, 1, cdh1).
term(cyca, 1, cyca).
term(cyca, 1, rb).
term(cyca, 2, cdc20).
term(cyca, 2, cyca).
term(cyca, 2, rb).
term(cyca, 2, ubch10).
term(cyca, 3, cdc20).
term(cyca, 3, cdh1).
term(cyca, 3, e2f).
term(cyca, 3, rb).
term(cyca, 4, cdc20).
term(cyca, 4, e2f).
term(cyca, 4, rb).
term(cyca, 4, ubch10).

%Regulators of cycb
regulates(cdc20, cycb, 1).
regulates(cdh1, cycb, 1).

%Regulatory function of cycb
function(cycb, 1).
term(cycb, 1, cdc20).
term(cycb, 1, cdh1).

%Regulators of cycd
regulates(cycd, cycd, 0).

%Regulatory function of cycd
function(cycd, 1).
term(cycd, 1, cycd).

%Regulators of cyce
regulates(rb, cyce, 1).
regulates(e2f, cyce, 0).

%Regulatory function of cyce
function(cyce, 1).
term(cyce, 1, e2f).
term(cyce, 1, rb).

%Regulators of e2f
regulates(rb, e2f, 1).
regulates(cyca, e2f, 1).
regulates(cycb, e2f, 1).
regulates(p27, e2f, 0).

%Regulatory function of e2f
function(e2f, 2).
term(e2f, 1, cyca).
term(e2f, 1, cycb).
term(e2f, 1, rb).
term(e2f, 2, cycb).
term(e2f, 2, p27).
term(e2f, 2, rb).

%Regulators of rb
regulates(cycd, rb, 1).
regulates(cyce, rb, 1).
regulates(cyca, rb, 1).
regulates(cycb, rb, 1).
regulates(p27, rb, 0).

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
regulates(cdc20, ubch10, 0).
regulates(ubch10, ubch10, 0).
regulates(cycb, ubch10, 0).
regulates(cyca, ubch10, 0).
regulates(cdh1, ubch10, 1).

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
regulates(cyca, cdh1, 1).
regulates(cycb, cdh1, 1).
regulates(p27, cdh1, 0).
regulates(cdc20, cdh1, 0).

%Regulatory function of cdh1
function(cdh1, 3).
term(cdh1, 1, cyca).
term(cdh1, 1, cycb).
term(cdh1, 2, cycb).
term(cdh1, 2, p27).
term(cdh1, 3, cdc20).

%Regulators of p27
regulates(cycd, p27, 1).
regulates(cyce, p27, 1).
regulates(cyca, p27, 1).
regulates(cycb, p27, 1).
regulates(p27, p27, 0).

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