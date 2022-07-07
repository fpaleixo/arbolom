%Compounds
compound(ap1).
compound(cd45).
compound(cd8).
compound(cre).
compound(creb).
compound(ca).
compound(calcin).
compound(dag).
compound(erk).
compound(fos).
compound(fyn).
compound(gads).
compound(grb2sos).
compound(ikk).
compound(ip3).
compound(ikb).
compound(itk).
compound(jnk).
compound(jun).
compound(lat).
compound(lck).
compound(mek).
compound(nfat).
compound(nfkb).
compound(pagcsk).
compound(pkcth).
compound(plcg_a).
compound(plcg_b).
compound(raf).
compound(ras).
compound(rasgrp1).
compound(rlk).
compound(rsk).
compound(sek).
compound(slp76).
compound(tcrbind).
compound(tcrlig).
compound(tcrphos).
compound(zap70).
compound(ccbl).

%Regulators of ap1
regulates(fos, ap1, 0).

%Regulatory function of ap1
function(ap1, 1).
term(ap1, 1, fos).

%Regulators of cd45
regulates(cd45, cd45, 0).

%Regulatory function of cd45
function(cd45, 1).
term(cd45, 1, cd45).

%Regulators of cd8
regulates(cd8, cd8, 0).

%Regulatory function of cd8
function(cd8, 1).
term(cd8, 1, cd8).

%Regulators of ca
regulates(ip3, ca, 0).
regulates(sek, ca, 0).

%Regulatory function of ca
function(ca, 2).
term(ca, 1, ip3).
term(ca, 2, sek).

%Regulators of calcin
regulates(ca, calcin, 0).

%Regulatory function of calcin
function(calcin, 1).
term(calcin, 1, ca).

%Regulators of dag
regulates(plcg_a, dag, 0).

%Regulatory function of dag
function(dag, 1).
term(dag, 1, plcg_a).

%Regulators of erk
regulates(mek, erk, 0).
regulates(ccbl, erk, 0).
regulates(dag, erk, 1).

%Regulatory function of erk
function(erk, 3).
term(erk, 1, mek).
term(erk, 2, ccbl).
term(erk, 3, dag).

%Regulators of fos
regulates(erk, fos, 0).
regulates(jun, fos, 1).

%Regulatory function of fos
function(fos, 1).
term(fos, 1, erk).
term(fos, 1, jun).

%Regulators of fyn
regulates(tcrbind, fyn, 0).
regulates(cd45, fyn, 0).
regulates(tcrlig, fyn, 0).

%Regulatory function of fyn
function(fyn, 3).
term(fyn, 1, tcrbind).
term(fyn, 2, cd45).
term(fyn, 3, tcrlig).

%Regulators of gads
regulates(cd45, gads, 1).

%Regulatory function of gads
function(gads, 1).
term(gads, 1, cd45).

%Regulators of ikk
regulates(cd45, ikk, 0).
regulates(cre, ikk, 0).

%Regulatory function of ikk
function(ikk, 1).
term(ikk, 1, cd45).
term(ikk, 1, cre).

%Regulators of ip3
regulates(cre, ip3, 0).

%Regulatory function of ip3
function(ip3, 1).
term(ip3, 1, cre).

%Regulators of itk
regulates(ap1, itk, 1).

%Regulatory function of itk
function(itk, 1).
term(itk, 1, ap1).

%Regulators of jnk
regulates(sek, jnk, 0).

%Regulatory function of jnk
function(jnk, 1).
term(jnk, 1, sek).

%Regulators of lat
regulates(zap70, lat, 0).

%Regulatory function of lat
function(lat, 1).
term(lat, 1, zap70).

%Regulators of lck
regulates(pagcsk, lck, 1).
regulates(cd8, lck, 0).
regulates(jnk, lck, 1).

%Regulatory function of lck
function(lck, 3).
term(lck, 1, pagcsk).
term(lck, 2, cd8).
term(lck, 3, jnk).

%Regulators of mek
regulates(raf, mek, 0).

%Regulatory function of mek
function(mek, 1).
term(mek, 1, raf).

%Regulators of nfat
regulates(cd45, nfat, 1).

%Regulatory function of nfat
function(nfat, 1).
term(nfat, 1, cd45).

%Regulators of pagcsk
regulates(tcrbind, pagcsk, 1).

%Regulatory function of pagcsk
function(pagcsk, 1).
term(pagcsk, 1, tcrbind).

%Regulators of pkcth
regulates(dag, pkcth, 0).
regulates(ca, pkcth, 1).
regulates(fos, pkcth, 0).

%Regulatory function of pkcth
function(pkcth, 3).
term(pkcth, 1, dag).
term(pkcth, 2, ca).
term(pkcth, 3, fos).

%Regulators of plcg_a
regulates(zap70, plcg_a, 0).
regulates(plcg_b, plcg_a, 0).
regulates(rlk, plcg_a, 0).
regulates(ap1, plcg_a, 1).
regulates(jnk, plcg_a, 0).

%Regulatory function of plcg_a
function(plcg_a, 1).
term(plcg_a, 1, ap1).
term(plcg_a, 1, jnk).
term(plcg_a, 1, plcg_b).
term(plcg_a, 1, rlk).
term(plcg_a, 1, zap70).

%Regulators of plcg_b
regulates(lat, plcg_b, 0).

%Regulatory function of plcg_b
function(plcg_b, 1).
term(plcg_b, 1, lat).

%Regulators of ras
regulates(rasgrp1, ras, 0).
regulates(ikb, ras, 1).

%Regulatory function of ras
function(ras, 1).
term(ras, 1, ikb).
term(ras, 1, rasgrp1).

%Regulators of rasgrp1
regulates(pkcth, rasgrp1, 0).

%Regulatory function of rasgrp1
function(rasgrp1, 1).
term(rasgrp1, 1, pkcth).

%Regulators of rlk
regulates(lck, rlk, 0).

%Regulatory function of rlk
function(rlk, 1).
term(rlk, 1, lck).

%Regulators of rsk
regulates(sek, rsk, 0).

%Regulatory function of rsk
function(rsk, 1).
term(rsk, 1, sek).

%Regulators of sek
regulates(pkcth, sek, 0).

%Regulatory function of sek
function(sek, 1).
term(sek, 1, pkcth).

%Regulators of tcrlig
regulates(mek, tcrlig, 1).

%Regulatory function of tcrlig
function(tcrlig, 1).
term(tcrlig, 1, mek).

%Regulators of tcrphos
regulates(ap1, tcrphos, 0).

%Regulatory function of tcrphos
function(tcrphos, 1).
term(tcrphos, 1, ap1).

%Regulators of zap70
regulates(ccbl, zap70, 1).

%Regulatory function of zap70
function(zap70, 1).
term(zap70, 1, ccbl).

%Regulators of ccbl
regulates(zap70, ccbl, 0).

%Regulatory function of ccbl
function(ccbl, 1).
term(ccbl, 1, zap70).

