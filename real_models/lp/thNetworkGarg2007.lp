%Compounds
node(gata3).
node(ifn_b).
node(ifn_br).
node(ifn_g).
node(ifn_gr).
node(il_10).
node(il_10r).
node(il_12).
node(il_12r).
node(il_18r).
node(il_4).
node(il_4r).
node(irak).
node(jak1).
node(nfat).
node(socs1).
node(stat1).
node(stat3).
node(stat4).
node(stat6).
node(t_bet).
node(tcr).

%Regulators of nfat
edge(tcr, nfat, 1).

%Regulatory function of nfat
function(nfat, 1).
term(nfat, 1, tcr).

%Regulators of ifn_br
edge(ifn_b, ifn_br, 1).

%Regulatory function of ifn_br
function(ifn_br, 1).
term(ifn_br, 1, ifn_b).

%Regulators of il_18r
edge(il_18r, il_18r, 1).
edge(stat6, il_18r, 0).

%Regulatory function of il_18r
function(il_18r, 1).
term(il_18r, 1, il_18r).
term(il_18r, 1, stat6).

%Regulators of irak
edge(il_18r, irak, 1).

%Regulatory function of irak
function(irak, 1).
term(irak, 1, il_18r).

%Regulators of socs1
edge(t_bet, socs1, 1).
edge(stat1, socs1, 1).

%Regulatory function of socs1
function(socs1, 2).
term(socs1, 1, t_bet).
term(socs1, 2, stat1).

%Regulators of il_12r
edge(il_12, il_12r, 1).
edge(stat6, il_12r, 0).

%Regulatory function of il_12r
function(il_12r, 1).
term(il_12r, 1, il_12).
term(il_12r, 1, stat6).

%Regulators of stat4
edge(il_12r, stat4, 1).
edge(gata3, stat4, 0).

%Regulatory function of stat4
function(stat4, 1).
term(stat4, 1, gata3).
term(stat4, 1, il_12r).

%Regulators of t_bet
edge(t_bet, t_bet, 1).
edge(gata3, t_bet, 0).
edge(stat1, t_bet, 1).

%Regulatory function of t_bet
function(t_bet, 2).
term(t_bet, 1, gata3).
term(t_bet, 1, t_bet).
term(t_bet, 2, gata3).
term(t_bet, 2, stat1).

%Regulators of ifn_g
edge(nfat, ifn_g, 1).
edge(stat3, ifn_g, 0).
edge(irak, ifn_g, 1).
edge(stat4, ifn_g, 1).
edge(t_bet, ifn_g, 1).

%Regulatory function of ifn_g
function(ifn_g, 4).
term(ifn_g, 1, nfat).
term(ifn_g, 1, stat3).
term(ifn_g, 2, irak).
term(ifn_g, 2, stat3).
term(ifn_g, 3, stat3).
term(ifn_g, 3, stat4).
term(ifn_g, 4, stat3).
term(ifn_g, 4, t_bet).

%Regulators of ifn_gr
edge(ifn_g, ifn_gr, 1).

%Regulatory function of ifn_gr
function(ifn_gr, 1).
term(ifn_gr, 1, ifn_g).

%Regulators of jak1
edge(ifn_gr, jak1, 1).
edge(socs1, jak1, 0).

%Regulatory function of jak1
function(jak1, 1).
term(jak1, 1, ifn_gr).
term(jak1, 1, socs1).

%Regulators of stat1
edge(jak1, stat1, 1).
edge(ifn_br, stat1, 1).

%Regulatory function of stat1
function(stat1, 2).
term(stat1, 1, jak1).
term(stat1, 2, ifn_br).

%Regulators of il_4
edge(stat1, il_4, 0).
edge(gata3, il_4, 1).

%Regulatory function of il_4
function(il_4, 1).
term(il_4, 1, gata3).
term(il_4, 1, stat1).

%Regulators of il_4r
edge(il_4, il_4r, 1).
edge(socs1, il_4r, 0).

%Regulatory function of il_4r
function(il_4r, 1).
term(il_4r, 1, il_4).
term(il_4r, 1, socs1).

%Regulators of stat6
edge(il_4r, stat6, 1).

%Regulatory function of stat6
function(stat6, 1).
term(stat6, 1, il_4r).

%Regulators of gata3
edge(stat6, gata3, 1).
edge(t_bet, gata3, 0).
edge(gata3, gata3, 1).

%Regulatory function of gata3
function(gata3, 2).
term(gata3, 1, stat6).
term(gata3, 1, t_bet).
term(gata3, 2, gata3).
term(gata3, 2, t_bet).

%Regulators of il_10
edge(gata3, il_10, 1).

%Regulatory function of il_10
function(il_10, 1).
term(il_10, 1, gata3).

%Regulators of il_10r
edge(il_10, il_10r, 1).

%Regulatory function of il_10r
function(il_10r, 1).
term(il_10r, 1, il_10).

%Regulators of stat3
edge(il_10r, stat3, 1).

%Regulatory function of stat3
function(stat3, 1).
term(stat3, 1, il_10r).

