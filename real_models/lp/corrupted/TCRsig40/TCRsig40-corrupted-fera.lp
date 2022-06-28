%Compounds
node(ap1).
node(cd45).
node(cd8).
node(cre).
node(creb).
node(ca).
node(calcin).
node(dag).
node(erk).
node(fos).
node(fyn).
node(gads).
node(grb2sos).
node(ikk).
node(ip3).
node(ikb).
node(itk).
node(jnk).
node(jun).
node(lat).
node(lck).
node(mek).
node(nfat).
node(nfkb).
node(pagcsk).
node(pkcth).
node(plcg_a).
node(plcg_b).
node(raf).
node(ras).
node(rasgrp1).
node(rlk).
node(rsk).
node(sek).
node(slp76).
node(tcrbind).
node(tcrlig).
node(tcrphos).
node(zap70).
node(ccbl).

%Regulators of ap1
edge(fos, ap1, 0).

%Regulatory function of ap1
function(ap1, 1).
term(ap1, 1, fos).

%Regulators of cd45
edge(cd45, cd45, 0).

%Regulatory function of cd45
function(cd45, 1).
term(cd45, 1, cd45).

%Regulators of cd8
edge(cd8, cd8, 0).

%Regulatory function of cd8
function(cd8, 1).
term(cd8, 1, cd8).

%Regulators of ca
edge(ip3, ca, 0).
edge(sek, ca, 0).

%Regulatory function of ca
function(ca, 2).
term(ca, 1, ip3).
term(ca, 2, sek).

%Regulators of calcin
edge(ca, calcin, 0).

%Regulatory function of calcin
function(calcin, 1).
term(calcin, 1, ca).

%Regulators of dag
edge(plcg_a, dag, 0).

%Regulatory function of dag
function(dag, 1).
term(dag, 1, plcg_a).

%Regulators of erk
edge(mek, erk, 0).
edge(ccbl, erk, 0).
edge(dag, erk, 1).

%Regulatory function of erk
function(erk, 3).
term(erk, 1, mek).
term(erk, 2, ccbl).
term(erk, 3, dag).

%Regulators of fos
edge(erk, fos, 0).
edge(jun, fos, 1).

%Regulatory function of fos
function(fos, 1).
term(fos, 1, erk).
term(fos, 1, jun).

%Regulators of fyn
edge(tcrbind, fyn, 0).
edge(cd45, fyn, 0).
edge(tcrlig, fyn, 0).

%Regulatory function of fyn
function(fyn, 3).
term(fyn, 1, tcrbind).
term(fyn, 2, cd45).
term(fyn, 3, tcrlig).

%Regulators of gads
edge(cd45, gads, 1).

%Regulatory function of gads
function(gads, 1).
term(gads, 1, cd45).

%Regulators of ikk
edge(cd45, ikk, 0).
edge(cre, ikk, 0).

%Regulatory function of ikk
function(ikk, 1).
term(ikk, 1, cd45).
term(ikk, 1, cre).

%Regulators of ip3
edge(cre, ip3, 0).

%Regulatory function of ip3
function(ip3, 1).
term(ip3, 1, cre).

%Regulators of itk
edge(ap1, itk, 1).

%Regulatory function of itk
function(itk, 1).
term(itk, 1, ap1).

%Regulators of jnk
edge(sek, jnk, 0).

%Regulatory function of jnk
function(jnk, 1).
term(jnk, 1, sek).

%Regulators of lat
edge(zap70, lat, 0).

%Regulatory function of lat
function(lat, 1).
term(lat, 1, zap70).

%Regulators of lck
edge(pagcsk, lck, 1).
edge(cd8, lck, 0).
edge(jnk, lck, 1).

%Regulatory function of lck
function(lck, 3).
term(lck, 1, pagcsk).
term(lck, 2, cd8).
term(lck, 3, jnk).

%Regulators of mek
edge(raf, mek, 0).

%Regulatory function of mek
function(mek, 1).
term(mek, 1, raf).

%Regulators of nfat
edge(cd45, nfat, 1).

%Regulatory function of nfat
function(nfat, 1).
term(nfat, 1, cd45).

%Regulators of pagcsk
edge(tcrbind, pagcsk, 1).

%Regulatory function of pagcsk
function(pagcsk, 1).
term(pagcsk, 1, tcrbind).

%Regulators of pkcth
edge(dag, pkcth, 0).
edge(ca, pkcth, 1).
edge(fos, pkcth, 0).

%Regulatory function of pkcth
function(pkcth, 3).
term(pkcth, 1, dag).
term(pkcth, 2, ca).
term(pkcth, 3, fos).

%Regulators of plcg_a
edge(zap70, plcg_a, 0).
edge(plcg_b, plcg_a, 0).
edge(rlk, plcg_a, 0).
edge(ap1, plcg_a, 1).
edge(jnk, plcg_a, 0).

%Regulatory function of plcg_a
function(plcg_a, 1).
term(plcg_a, 1, ap1).
term(plcg_a, 1, jnk).
term(plcg_a, 1, plcg_b).
term(plcg_a, 1, rlk).
term(plcg_a, 1, zap70).

%Regulators of plcg_b
edge(lat, plcg_b, 0).

%Regulatory function of plcg_b
function(plcg_b, 1).
term(plcg_b, 1, lat).

%Regulators of ras
edge(rasgrp1, ras, 0).
edge(ikb, ras, 1).

%Regulatory function of ras
function(ras, 1).
term(ras, 1, ikb).
term(ras, 1, rasgrp1).

%Regulators of rasgrp1
edge(pkcth, rasgrp1, 0).

%Regulatory function of rasgrp1
function(rasgrp1, 1).
term(rasgrp1, 1, pkcth).

%Regulators of rlk
edge(lck, rlk, 0).

%Regulatory function of rlk
function(rlk, 1).
term(rlk, 1, lck).

%Regulators of rsk
edge(sek, rsk, 0).

%Regulatory function of rsk
function(rsk, 1).
term(rsk, 1, sek).

%Regulators of sek
edge(pkcth, sek, 0).

%Regulatory function of sek
function(sek, 1).
term(sek, 1, pkcth).

%Regulators of tcrlig
edge(mek, tcrlig, 1).

%Regulatory function of tcrlig
function(tcrlig, 1).
term(tcrlig, 1, mek).

%Regulators of tcrphos
edge(ap1, tcrphos, 0).

%Regulatory function of tcrphos
function(tcrphos, 1).
term(tcrphos, 1, ap1).

%Regulators of zap70
edge(ccbl, zap70, 1).

%Regulatory function of zap70
function(zap70, 1).
term(zap70, 1, ccbl).

%Regulators of ccbl
edge(zap70, ccbl, 0).

%Regulatory function of ccbl
function(ccbl, 1).
term(ccbl, 1, zap70).

