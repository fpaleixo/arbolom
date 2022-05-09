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
edge(fos, ap1, 1).
edge(jun, ap1, 1).

%Regulatory function of ap1
function(ap1, 1).
term(ap1, 1, fos).
term(ap1, 1, jun).

%Regulators of cd45
edge(cd45, cd45, 1).

%Regulatory function of cd45
function(cd45, 1).
term(cd45, 1, cd45).

%Regulators of cd8
edge(cd8, cd8, 1).

%Regulatory function of cd8
function(cd8, 1).
term(cd8, 1, cd8).

%Regulators of cre
edge(creb, cre, 1).

%Regulatory function of cre
function(cre, 1).
term(cre, 1, creb).

%Regulators of creb
edge(rsk, creb, 1).

%Regulatory function of creb
function(creb, 1).
term(creb, 1, rsk).

%Regulators of ca
edge(ip3, ca, 1).

%Regulatory function of ca
function(ca, 1).
term(ca, 1, ip3).

%Regulators of calcin
edge(ca, calcin, 1).

%Regulatory function of calcin
function(calcin, 1).
term(calcin, 1, ca).

%Regulators of dag
edge(plcg_a, dag, 1).

%Regulatory function of dag
function(dag, 1).
term(dag, 1, plcg_a).

%Regulators of erk
edge(mek, erk, 1).

%Regulatory function of erk
function(erk, 1).
term(erk, 1, mek).

%Regulators of fos
edge(erk, fos, 1).

%Regulatory function of fos
function(fos, 1).
term(fos, 1, erk).

%Regulators of fyn
edge(cd45, fyn, 1).
edge(lck, fyn, 1).
edge(tcrbind, fyn, 1).

%Regulatory function of fyn
function(fyn, 2).
term(fyn, 1, cd45).
term(fyn, 1, lck).
term(fyn, 2, cd45).
term(fyn, 2, tcrbind).

%Regulators of gads
edge(lat, gads, 1).

%Regulatory function of gads
function(gads, 1).
term(gads, 1, lat).

%Regulators of grb2sos
edge(lat, grb2sos, 1).

%Regulatory function of grb2sos
function(grb2sos, 1).
term(grb2sos, 1, lat).

%Regulators of ikk
edge(pkcth, ikk, 1).

%Regulatory function of ikk
function(ikk, 1).
term(ikk, 1, pkcth).

%Regulators of ip3
edge(plcg_a, ip3, 1).

%Regulatory function of ip3
function(ip3, 1).
term(ip3, 1, plcg_a).

%Regulators of ikb
edge(ikk, ikb, 0).

%Regulatory function of ikb
function(ikb, 1).
term(ikb, 1, ikk).

%Regulators of itk
edge(zap70, itk, 1).
edge(slp76, itk, 1).

%Regulatory function of itk
function(itk, 1).
term(itk, 1, slp76).
term(itk, 1, zap70).

%Regulators of jnk
edge(sek, jnk, 1).

%Regulatory function of jnk
function(jnk, 1).
term(jnk, 1, sek).

%Regulators of jun
edge(jnk, jun, 1).

%Regulatory function of jun
function(jun, 1).
term(jun, 1, jnk).

%Regulators of lat
edge(zap70, lat, 1).

%Regulatory function of lat
function(lat, 1).
term(lat, 1, zap70).

%Regulators of lck
edge(cd45, lck, 1).
edge(cd8, lck, 1).
edge(pagcsk, lck, 0).

%Regulatory function of lck
function(lck, 1).
term(lck, 1, cd45).
term(lck, 1, cd8).
term(lck, 1, pagcsk).

%Regulators of mek
edge(raf, mek, 1).

%Regulatory function of mek
function(mek, 1).
term(mek, 1, raf).

%Regulators of nfat
edge(calcin, nfat, 1).

%Regulatory function of nfat
function(nfat, 1).
term(nfat, 1, calcin).

%Regulators of nfkb
edge(ikb, nfkb, 0).

%Regulatory function of nfkb
function(nfkb, 1).
term(nfkb, 1, ikb).

%Regulators of pagcsk
edge(tcrbind, pagcsk, 0).

%Regulatory function of pagcsk
function(pagcsk, 1).
term(pagcsk, 1, tcrbind).

%Regulators of pkcth
edge(dag, pkcth, 1).

%Regulatory function of pkcth
function(pkcth, 1).
term(pkcth, 1, dag).

%Regulators of plcg_a
edge(zap70, plcg_a, 1).
edge(itk, plcg_a, 1).
edge(slp76, plcg_a, 1).
edge(plcg_b, plcg_a, 1).
edge(rlk, plcg_a, 1).

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
edge(lat, plcg_b, 1).

%Regulatory function of plcg_b
function(plcg_b, 1).
term(plcg_b, 1, lat).

%Regulators of raf
edge(ras, raf, 1).

%Regulatory function of raf
function(raf, 1).
term(raf, 1, ras).

%Regulators of ras
edge(grb2sos, ras, 1).
edge(rasgrp1, ras, 1).

%Regulatory function of ras
function(ras, 1).
term(ras, 1, grb2sos).
term(ras, 1, rasgrp1).

%Regulators of rasgrp1
edge(dag, rasgrp1, 1).
edge(pkcth, rasgrp1, 1).

%Regulatory function of rasgrp1
function(rasgrp1, 1).
term(rasgrp1, 1, dag).
term(rasgrp1, 1, pkcth).

%Regulators of rlk
edge(lck, rlk, 1).

%Regulatory function of rlk
function(rlk, 1).
term(rlk, 1, lck).

%Regulators of rsk
edge(erk, rsk, 1).

%Regulatory function of rsk
function(rsk, 1).
term(rsk, 1, erk).

%Regulators of sek
edge(pkcth, sek, 1).

%Regulatory function of sek
function(sek, 1).
term(sek, 1, pkcth).

%Regulators of slp76
edge(gads, slp76, 1).

%Regulatory function of slp76
function(slp76, 1).
term(slp76, 1, gads).

%Regulators of tcrbind
edge(tcrlig, tcrbind, 1).
edge(ccbl, tcrbind, 0).

%Regulatory function of tcrbind
function(tcrbind, 1).
term(tcrbind, 1, ccbl).
term(tcrbind, 1, tcrlig).

%Regulators of tcrlig
edge(tcrlig, tcrlig, 1).

%Regulatory function of tcrlig
function(tcrlig, 1).
term(tcrlig, 1, tcrlig).

%Regulators of tcrphos
edge(tcrbind, tcrphos, 1).
edge(lck, tcrphos, 1).
edge(fyn, tcrphos, 1).

%Regulatory function of tcrphos
function(tcrphos, 2).
term(tcrphos, 1, lck).
term(tcrphos, 1, tcrbind).
term(tcrphos, 2, fyn).

%Regulators of zap70
edge(lck, zap70, 1).
edge(ccbl, zap70, 0).
edge(tcrphos, zap70, 1).

%Regulatory function of zap70
function(zap70, 1).
term(zap70, 1, ccbl).
term(zap70, 1, lck).
term(zap70, 1, tcrphos).

%Regulators of ccbl
edge(zap70, ccbl, 1).

%Regulatory function of ccbl
function(ccbl, 1).
term(ccbl, 1, zap70).

