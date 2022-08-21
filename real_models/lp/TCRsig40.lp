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
regulates(jun, ap1, 0).

%Regulatory function of ap1
function(ap1, 1).
term(ap1, 1, fos).
term(ap1, 1, jun).

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

%Regulators of cre
regulates(creb, cre, 0).

%Regulatory function of cre
function(cre, 1).
term(cre, 1, creb).

%Regulators of creb
regulates(rsk, creb, 0).

%Regulatory function of creb
function(creb, 1).
term(creb, 1, rsk).

%Regulators of ca
regulates(ip3, ca, 0).

%Regulatory function of ca
function(ca, 1).
term(ca, 1, ip3).

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

%Regulatory function of erk
function(erk, 1).
term(erk, 1, mek).

%Regulators of fos
regulates(erk, fos, 0).

%Regulatory function of fos
function(fos, 1).
term(fos, 1, erk).

%Regulators of fyn
regulates(cd45, fyn, 0).
regulates(lck, fyn, 0).
regulates(tcrbind, fyn, 0).

%Regulatory function of fyn
function(fyn, 2).
term(fyn, 1, cd45).
term(fyn, 1, lck).
term(fyn, 2, cd45).
term(fyn, 2, tcrbind).

%Regulators of gads
regulates(lat, gads, 0).

%Regulatory function of gads
function(gads, 1).
term(gads, 1, lat).

%Regulators of grb2sos
regulates(lat, grb2sos, 0).

%Regulatory function of grb2sos
function(grb2sos, 1).
term(grb2sos, 1, lat).

%Regulators of ikk
regulates(pkcth, ikk, 0).

%Regulatory function of ikk
function(ikk, 1).
term(ikk, 1, pkcth).

%Regulators of ip3
regulates(plcg_a, ip3, 0).

%Regulatory function of ip3
function(ip3, 1).
term(ip3, 1, plcg_a).

%Regulators of ikb
regulates(ikk, ikb, 1).

%Regulatory function of ikb
function(ikb, 1).
term(ikb, 1, ikk).

%Regulators of itk
regulates(zap70, itk, 0).
regulates(slp76, itk, 0).

%Regulatory function of itk
function(itk, 1).
term(itk, 1, slp76).
term(itk, 1, zap70).

%Regulators of jnk
regulates(sek, jnk, 0).

%Regulatory function of jnk
function(jnk, 1).
term(jnk, 1, sek).

%Regulators of jun
regulates(jnk, jun, 0).

%Regulatory function of jun
function(jun, 1).
term(jun, 1, jnk).

%Regulators of lat
regulates(zap70, lat, 0).

%Regulatory function of lat
function(lat, 1).
term(lat, 1, zap70).

%Regulators of lck
regulates(cd45, lck, 0).
regulates(cd8, lck, 0).
regulates(pagcsk, lck, 1).

%Regulatory function of lck
function(lck, 1).
term(lck, 1, cd45).
term(lck, 1, cd8).
term(lck, 1, pagcsk).

%Regulators of mek
regulates(raf, mek, 0).

%Regulatory function of mek
function(mek, 1).
term(mek, 1, raf).

%Regulators of nfat
regulates(calcin, nfat, 0).

%Regulatory function of nfat
function(nfat, 1).
term(nfat, 1, calcin).

%Regulators of nfkb
regulates(ikb, nfkb, 1).

%Regulatory function of nfkb
function(nfkb, 1).
term(nfkb, 1, ikb).

%Regulators of pagcsk
regulates(tcrbind, pagcsk, 1).

%Regulatory function of pagcsk
function(pagcsk, 1).
term(pagcsk, 1, tcrbind).

%Regulators of pkcth
regulates(dag, pkcth, 0).

%Regulatory function of pkcth
function(pkcth, 1).
term(pkcth, 1, dag).

%Regulators of plcg_a
regulates(zap70, plcg_a, 0).
regulates(itk, plcg_a, 0).
regulates(slp76, plcg_a, 0).
regulates(plcg_b, plcg_a, 0).
regulates(rlk, plcg_a, 0).

%Regulatory function of plcg_a
function(plcg_a, 2).
term(plcg_a, 1, itk).
term(plcg_a, 1, plcg_b).
term(plcg_a, 1, slp76).
term(plcg_a, 1, zap70).
term(plcg_a, 2, plcg_b).
term(plcg_a, 2, rlk).
term(plcg_a, 2, slp76).
term(plcg_a, 2, zap70).

%Regulators of plcg_b
regulates(lat, plcg_b, 0).

%Regulatory function of plcg_b
function(plcg_b, 1).
term(plcg_b, 1, lat).

%Regulators of raf
regulates(ras, raf, 0).

%Regulatory function of raf
function(raf, 1).
term(raf, 1, ras).

%Regulators of ras
regulates(grb2sos, ras, 0).
regulates(rasgrp1, ras, 0).

%Regulatory function of ras
function(ras, 1).
term(ras, 1, grb2sos).
term(ras, 1, rasgrp1).

%Regulators of rasgrp1
regulates(dag, rasgrp1, 0).
regulates(pkcth, rasgrp1, 0).

%Regulatory function of rasgrp1
function(rasgrp1, 1).
term(rasgrp1, 1, dag).
term(rasgrp1, 1, pkcth).

%Regulators of rlk
regulates(lck, rlk, 0).

%Regulatory function of rlk
function(rlk, 1).
term(rlk, 1, lck).

%Regulators of rsk
regulates(erk, rsk, 0).

%Regulatory function of rsk
function(rsk, 1).
term(rsk, 1, erk).

%Regulators of sek
regulates(pkcth, sek, 0).

%Regulatory function of sek
function(sek, 1).
term(sek, 1, pkcth).

%Regulators of slp76
regulates(gads, slp76, 0).

%Regulatory function of slp76
function(slp76, 1).
term(slp76, 1, gads).

%Regulators of tcrbind
regulates(tcrlig, tcrbind, 0).
regulates(ccbl, tcrbind, 1).

%Regulatory function of tcrbind
function(tcrbind, 1).
term(tcrbind, 1, ccbl).
term(tcrbind, 1, tcrlig).

%Regulators of tcrlig
regulates(tcrlig, tcrlig, 0).

%Regulatory function of tcrlig
function(tcrlig, 1).
term(tcrlig, 1, tcrlig).

%Regulators of tcrphos
regulates(tcrbind, tcrphos, 0).
regulates(lck, tcrphos, 0).
regulates(fyn, tcrphos, 0).

%Regulatory function of tcrphos
function(tcrphos, 2).
term(tcrphos, 1, lck).
term(tcrphos, 1, tcrbind).
term(tcrphos, 2, fyn).

%Regulators of zap70
regulates(lck, zap70, 0).
regulates(ccbl, zap70, 1).
regulates(tcrphos, zap70, 0).

%Regulatory function of zap70
function(zap70, 1).
term(zap70, 1, ccbl).
term(zap70, 1, lck).
term(zap70, 1, tcrphos).

%Regulators of ccbl
regulates(zap70, ccbl, 0).

%Regulatory function of ccbl
function(ccbl, 1).
term(ccbl, 1, zap70).

