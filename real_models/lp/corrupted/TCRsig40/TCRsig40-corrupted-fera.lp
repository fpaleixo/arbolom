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
regulates(tcrlig, ap1, 0).

%Regulatory function of ap1
function(ap1, 2).
term(ap1, 1, fos).
term(ap1, 2, tcrlig).

%Regulators of cd45
regulates(cd45, cd45, 1).

%Regulatory function of cd45
function(cd45, 1).
term(cd45, 1, cd45).

%Regulators of cd8
regulates(cd8, cd8, 0).
regulates(sek, cd8, 1).

%Regulatory function of cd8
function(cd8, 1).
term(cd8, 1, cd8).
term(cd8, 1, sek).

%Regulators of cre
regulates(creb, cre, 1).

%Regulatory function of cre
function(cre, 1).
term(cre, 1, creb).

%Regulators of creb
regulates(rsk, creb, 0).
regulates(ikk, creb, 1).

%Regulatory function of creb
function(creb, 1).
term(creb, 1, ikk).
term(creb, 1, rsk).

%Regulators of ca
regulates(ip3, ca, 1).

%Regulatory function of ca
function(ca, 1).
term(ca, 1, ip3).

%Regulators of calcin
regulates(ca, calcin, 1).

%Regulatory function of calcin
function(calcin, 1).
term(calcin, 1, ca).

%Regulators of dag
regulates(plcg_a, dag, 1).

%Regulatory function of dag
function(dag, 1).
term(dag, 1, plcg_a).

%Regulators of erk
regulates(mek, erk, 1).

%Regulatory function of erk
function(erk, 1).
term(erk, 1, mek).

%Regulators of fos
regulates(erk, fos, 0).
regulates(lat, fos, 0).
regulates(plcg_a, fos, 1).

%Regulatory function of fos
function(fos, 3).
term(fos, 1, erk).
term(fos, 2, lat).
term(fos, 3, plcg_a).

%Regulators of fyn
regulates(cd45, fyn, 1).
regulates(lck, fyn, 1).
regulates(tcrbind, fyn, 0).

%Regulatory function of fyn
function(fyn, 2).
term(fyn, 1, cd45).
term(fyn, 1, lck).
term(fyn, 2, cd45).
term(fyn, 2, tcrbind).

%Regulators of gads
regulates(lat, gads, 1).

%Regulatory function of gads
function(gads, 1).
term(gads, 1, lat).

%Regulators of grb2sos
regulates(lat, grb2sos, 1).

%Regulatory function of grb2sos
function(grb2sos, 1).
term(grb2sos, 1, lat).

%Regulators of ikk
regulates(pkcth, ikk, 1).
regulates(tcrphos, ikk, 0).

%Regulatory function of ikk
function(ikk, 1).
term(ikk, 1, pkcth).
term(ikk, 1, tcrphos).

%Regulators of ip3
regulates(ip3, ip3, 0).

%Regulatory function of ip3
function(ip3, 1).
term(ip3, 1, ip3).

%Regulators of ikb
regulates(ikk, ikb, 1).
regulates(cd8, ikb, 1).

%Regulatory function of ikb
function(ikb, 2).
term(ikb, 1, ikk).
term(ikb, 2, cd8).

%Regulators of itk
regulates(zap70, itk, 1).
regulates(ca, itk, 1).
regulates(rasgrp1, itk, 0).

%Regulatory function of itk
function(itk, 2).
term(itk, 1, zap70).
term(itk, 2, ca).
term(itk, 2, rasgrp1).

%Regulators of jnk
regulates(sek, jnk, 1).
regulates(fyn, jnk, 0).
regulates(zap70, jnk, 0).

%Regulatory function of jnk
function(jnk, 3).
term(jnk, 1, sek).
term(jnk, 2, fyn).
term(jnk, 3, zap70).

%Regulators of jun
regulates(jnk, jun, 0).
regulates(slp76, jun, 1).

%Regulatory function of jun
function(jun, 1).
term(jun, 1, jnk).
term(jun, 1, slp76).

%Regulators of lat
regulates(zap70, lat, 0).
regulates(cd45, lat, 0).

%Regulatory function of lat
function(lat, 1).
term(lat, 1, cd45).
term(lat, 1, zap70).

%Regulators of lck
regulates(cd45, lck, 1).

%Regulatory function of lck
function(lck, 1).
term(lck, 1, cd45).

%Regulators of mek
regulates(raf, mek, 0).
regulates(ip3, mek, 1).

%Regulatory function of mek
function(mek, 1).
term(mek, 1, ip3).
term(mek, 1, raf).

%Regulators of nfat
regulates(calcin, nfat, 1).

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
regulates(pkcth, pkcth, 0).

%Regulatory function of pkcth
function(pkcth, 1).
term(pkcth, 1, pkcth).

%Regulators of plcg_a
regulates(slp76, plcg_a, 0).
regulates(plcg_b, plcg_a, 0).

%Regulatory function of plcg_a
function(plcg_a, 1).
term(plcg_a, 1, plcg_b).
term(plcg_a, 1, slp76).

%Regulators of plcg_b
regulates(plcg_b, plcg_b, 0).

%Regulatory function of plcg_b
function(plcg_b, 1).
term(plcg_b, 1, plcg_b).

%Regulators of raf
regulates(cd45, raf, 0).

%Regulatory function of raf
function(raf, 1).
term(raf, 1, cd45).

%Regulators of ras
regulates(cd45, ras, 0).

%Regulatory function of ras
function(ras, 1).
term(ras, 1, cd45).

%Regulators of rasgrp1
regulates(dag, rasgrp1, 1).
regulates(cd45, rasgrp1, 0).
regulates(pkcth, rasgrp1, 0).

%Regulatory function of rasgrp1
function(rasgrp1, 2).
term(rasgrp1, 1, cd45).
term(rasgrp1, 1, dag).
term(rasgrp1, 2, cd45).
term(rasgrp1, 2, pkcth).

%Regulators of rlk
regulates(rlk, rlk, 0).

%Regulatory function of rlk
function(rlk, 1).
term(rlk, 1, rlk).

%Regulators of rsk
regulates(erk, rsk, 1).

%Regulatory function of rsk
function(rsk, 1).
term(rsk, 1, erk).

%Regulators of sek
regulates(zap70, sek, 1).

%Regulatory function of sek
function(sek, 1).
term(sek, 1, zap70).

%Regulators of slp76
regulates(rlk, slp76, 1).

%Regulatory function of slp76
function(slp76, 1).
term(slp76, 1, rlk).

%Regulators of tcrbind
regulates(tcrlig, tcrbind, 1).
regulates(gads, tcrbind, 1).
regulates(ccbl, tcrbind, 1).

%Regulatory function of tcrbind
function(tcrbind, 2).
term(tcrbind, 1, gads).
term(tcrbind, 1, tcrlig).
term(tcrbind, 2, ccbl).
term(tcrbind, 2, gads).

%Regulators of tcrlig
regulates(tcrlig, tcrlig, 1).

%Regulatory function of tcrlig
function(tcrlig, 1).
term(tcrlig, 1, tcrlig).

%Regulators of tcrphos
regulates(lck, tcrphos, 1).
regulates(fyn, tcrphos, 1).

%Regulatory function of tcrphos
function(tcrphos, 2).
term(tcrphos, 1, lck).
term(tcrphos, 2, fyn).

%Regulators of zap70
regulates(lck, zap70, 1).
regulates(raf, zap70, 1).
regulates(ccbl, zap70, 1).

%Regulatory function of zap70
function(zap70, 2).
term(zap70, 1, lck).
term(zap70, 1, raf).
term(zap70, 2, ccbl).

%Regulators of ccbl
regulates(zap70, ccbl, 1).
regulates(grb2sos, ccbl, 0).
regulates(rasgrp1, ccbl, 1).

%Regulatory function of ccbl
function(ccbl, 3).
term(ccbl, 1, zap70).
term(ccbl, 2, grb2sos).
term(ccbl, 3, rasgrp1).

