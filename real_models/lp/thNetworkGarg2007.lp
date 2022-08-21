%Compounds
compound(nfat).
compound(ifn_br).
compound(il_18r).
compound(irak).
compound(socs1).
compound(il_12r).
compound(stat4).
compound(t_bet).
compound(ifn_g).
compound(ifn_gr).
compound(jak1).
compound(stat1).
compound(il_4).
compound(il_4r).
compound(stat6).
compound(gata3).
compound(il_10).
compound(il_10r).
compound(stat3).
compound(ifn_b).
compound(tcr).
compound(il_12).
compound(il_18).

%Regulators of nfat
regulates(tcr, nfat, 0).

%Regulatory function of nfat
function(nfat, 1).
term(nfat, 1, tcr).

%Regulators of ifn_br
regulates(ifn_b, ifn_br, 0).

%Regulatory function of ifn_br
function(ifn_br, 1).
term(ifn_br, 1, ifn_b).

%Regulators of il_18r
regulates(il_18, il_18r, 0).
regulates(stat6, il_18r, 1).

%Regulatory function of il_18r
function(il_18r, 1).
term(il_18r, 1, il_18).
term(il_18r, 1, stat6).

%Regulators of irak
regulates(il_18r, irak, 0).

%Regulatory function of irak
function(irak, 1).
term(irak, 1, il_18r).

%Regulators of socs1
regulates(t_bet, socs1, 0).
regulates(stat1, socs1, 0).

%Regulatory function of socs1
function(socs1, 2).
term(socs1, 1, t_bet).
term(socs1, 2, stat1).

%Regulators of il_12r
regulates(il_12, il_12r, 0).
regulates(stat6, il_12r, 1).

%Regulatory function of il_12r
function(il_12r, 1).
term(il_12r, 1, il_12).
term(il_12r, 1, stat6).

%Regulators of stat4
regulates(il_12r, stat4, 0).
regulates(gata3, stat4, 1).

%Regulatory function of stat4
function(stat4, 1).
term(stat4, 1, gata3).
term(stat4, 1, il_12r).

%Regulators of t_bet
regulates(t_bet, t_bet, 0).
regulates(gata3, t_bet, 1).
regulates(stat1, t_bet, 0).

%Regulatory function of t_bet
function(t_bet, 2).
term(t_bet, 1, gata3).
term(t_bet, 1, t_bet).
term(t_bet, 2, gata3).
term(t_bet, 2, stat1).

%Regulators of ifn_g
regulates(nfat, ifn_g, 0).
regulates(stat3, ifn_g, 1).
regulates(irak, ifn_g, 0).
regulates(stat4, ifn_g, 0).
regulates(t_bet, ifn_g, 0).

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
regulates(ifn_g, ifn_gr, 0).

%Regulatory function of ifn_gr
function(ifn_gr, 1).
term(ifn_gr, 1, ifn_g).

%Regulators of jak1
regulates(ifn_gr, jak1, 0).
regulates(socs1, jak1, 1).

%Regulatory function of jak1
function(jak1, 1).
term(jak1, 1, ifn_gr).
term(jak1, 1, socs1).

%Regulators of stat1
regulates(jak1, stat1, 0).
regulates(ifn_br, stat1, 0).

%Regulatory function of stat1
function(stat1, 2).
term(stat1, 1, jak1).
term(stat1, 2, ifn_br).

%Regulators of il_4
regulates(stat1, il_4, 1).
regulates(gata3, il_4, 0).

%Regulatory function of il_4
function(il_4, 1).
term(il_4, 1, gata3).
term(il_4, 1, stat1).

%Regulators of il_4r
regulates(il_4, il_4r, 0).
regulates(socs1, il_4r, 1).

%Regulatory function of il_4r
function(il_4r, 1).
term(il_4r, 1, il_4).
term(il_4r, 1, socs1).

%Regulators of stat6
regulates(il_4r, stat6, 0).

%Regulatory function of stat6
function(stat6, 1).
term(stat6, 1, il_4r).

%Regulators of gata3
regulates(stat6, gata3, 0).
regulates(t_bet, gata3, 1).
regulates(gata3, gata3, 0).

%Regulatory function of gata3
function(gata3, 2).
term(gata3, 1, stat6).
term(gata3, 1, t_bet).
term(gata3, 2, gata3).
term(gata3, 2, t_bet).

%Regulators of il_10
regulates(gata3, il_10, 0).

%Regulatory function of il_10
function(il_10, 1).
term(il_10, 1, gata3).

%Regulators of il_10r
regulates(il_10, il_10r, 0).

%Regulatory function of il_10r
function(il_10r, 1).
term(il_10r, 1, il_10).

%Regulators of stat3
regulates(il_10r, stat3, 0).

%Regulatory function of stat3
function(stat3, 1).
term(stat3, 1, il_10r).

%Regulators of ifn_b
regulates(ifn_b, ifn_b, 0).

%Regulatory function of ifn_b
function(ifn_b, 1).
term(ifn_b, 1, ifn_b).

%Regulators of tcr
regulates(tcr, tcr, 0).

%Regulatory function of tcr
function(tcr, 1).
term(tcr, 1, tcr).

%Regulators of il_12
regulates(il_12, il_12, 0).

%Regulatory function of il_12
function(il_12, 1).
term(il_12, 1, il_12).

%Regulators of il_18
regulates(il_18, il_18, 0).

%Regulatory function of il_18
function(il_18, 1).
term(il_18, 1, il_18).

