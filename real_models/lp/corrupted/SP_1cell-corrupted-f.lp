%Compounds
node(ci1).
node(ciact_b1).
node(ciact_b2).
node(cirep).
node(dsh).
node(en).
node(fz).
node(hh).
node(hh_ext).
node(nkd_b1).
node(nkd_b2).
node(pka_b1).
node(pka_b2).
node(ptc_b1).
node(ptc_b2).
node(slp).
node(wg_b1).
node(wg_b2).
node(wg_ext).

%Regulators of ci1
edge(en, ci1, 0).

%Regulatory function of ci1
function(ci1, 1).
term(ci1, 1, en).

%Regulators of ciact_b1
edge(ci1, ciact_b1, 1).
edge(pka_b1, ciact_b1, 0).
edge(ciact_b1, ciact_b1, 1).
edge(ciact_b2, ciact_b1, 1).
edge(dsh, ciact_b1, 1).

%Regulatory function of ciact_b1
function(ciact_b1, 3).
term(ciact_b1, 1, ci1).
term(ciact_b1, 1, pka_b1).
term(ciact_b1, 2, ciact_b1).
term(ciact_b1, 2, ciact_b2).
term(ciact_b1, 3, ci1).
term(ciact_b1, 3, dsh).

%Regulators of ciact_b2
edge(dsh, ciact_b2, 1).
edge(ci1, ciact_b2, 1).
edge(ciact_b1, ciact_b2, 1).
edge(pka_b1, ciact_b2, 0).

%Regulatory function of ciact_b2
function(ciact_b2, 1).
term(ciact_b2, 1, ci1).
term(ciact_b2, 1, ciact_b1).
term(ciact_b2, 1, dsh).
term(ciact_b2, 1, pka_b1).

%Regulators of cirep
edge(dsh, cirep, 0).
edge(ci1, cirep, 1).
edge(pka_b1, cirep, 1).
edge(pka_b2, cirep, 1).

%Regulatory function of cirep
function(cirep, 1).
term(cirep, 1, ci1).
term(cirep, 1, dsh).
term(cirep, 1, pka_b1).
term(cirep, 1, pka_b2).

%Regulators of dsh
edge(fz, dsh, 1).

%Regulatory function of dsh
function(dsh, 1).
term(dsh, 1, fz).

%Regulators of en
edge(dsh, en, 1).
edge(slp, en, 0).

%Regulatory function of en
function(en, 1).
term(en, 1, dsh).
term(en, 1, slp).

%Regulators of fz
edge(wg_ext, fz, 1).
edge(wg_b1, fz, 1).

%Regulatory function of fz
function(fz, 1).
term(fz, 1, wg_b1).
term(fz, 1, wg_ext).

%Regulators of hh
edge(en, hh, 1).
edge(cirep, hh, 0).

%Regulatory function of hh
function(hh, 1).
term(hh, 1, cirep).
term(hh, 1, en).

%Regulators of hh_ext
edge(hh_ext, hh_ext, 1).

%Regulatory function of hh_ext
function(hh_ext, 1).
term(hh_ext, 1, hh_ext).

%Regulators of nkd_b1
edge(nkd_b1, nkd_b1, 1).
edge(nkd_b2, nkd_b1, 1).
edge(en, nkd_b1, 0).

%Regulatory function of nkd_b1
function(nkd_b1, 2).
term(nkd_b1, 1, nkd_b1).
term(nkd_b1, 1, nkd_b2).
term(nkd_b1, 2, en).

%Regulators of nkd_b2
edge(dsh, nkd_b2, 1).
edge(nkd_b1, nkd_b2, 1).
edge(en, nkd_b2, 0).

%Regulatory function of nkd_b2
function(nkd_b2, 1).
term(nkd_b2, 1, dsh).
term(nkd_b2, 1, en).
term(nkd_b2, 1, nkd_b1).

%Regulators of pka_b1
edge(pka_b1, pka_b1, 1).
edge(pka_b2, pka_b1, 1).
edge(ptc_b1, pka_b1, 1).

%Regulatory function of pka_b1
function(pka_b1, 2).
term(pka_b1, 1, pka_b1).
term(pka_b1, 1, pka_b2).
term(pka_b1, 2, ptc_b1).

%Regulators of pka_b2
edge(pka_b1, pka_b2, 1).
edge(ptc_b1, pka_b2, 1).

%Regulatory function of pka_b2
function(pka_b2, 1).
term(pka_b2, 1, pka_b1).
term(pka_b2, 1, ptc_b1).

%Regulators of ptc_b1
edge(en, ptc_b1, 0).
edge(hh_ext, ptc_b1, 0).
edge(ptc_b1, ptc_b1, 1).
edge(ptc_b2, ptc_b1, 1).

%Regulatory function of ptc_b1
function(ptc_b1, 2).
term(ptc_b1, 1, en).
term(ptc_b1, 1, hh_ext).
term(ptc_b1, 2, ptc_b1).
term(ptc_b1, 2, ptc_b2).

%Regulators of ptc_b2
edge(en, ptc_b2, 0).
edge(ciact_b1, ptc_b2, 1).
edge(ptc_b1, ptc_b2, 1).
edge(hh_ext, ptc_b2, 0).

%Regulatory function of ptc_b2
function(ptc_b2, 1).
term(ptc_b2, 1, ciact_b1).
term(ptc_b2, 1, en).
term(ptc_b2, 1, hh_ext).
term(ptc_b2, 1, ptc_b1).

%Regulators of slp
edge(dsh, slp, 1).
edge(en, slp, 0).

%Regulatory function of slp
function(slp, 1).
term(slp, 1, dsh).
term(slp, 1, en).

%Regulators of wg_b1
edge(slp, wg_b1, 1).
edge(nkd_b1, wg_b1, 0).
edge(en, wg_b1, 0).
edge(ciact_b1, wg_b1, 1).
edge(nkd_b2, wg_b1, 0).
edge(ciact_b2, wg_b1, 1).
edge(wg_b1, wg_b1, 1).
edge(wg_b2, wg_b1, 1).

%Regulatory function of wg_b1
function(wg_b1, 4).
term(wg_b1, 1, ciact_b1).
term(wg_b1, 1, en).
term(wg_b1, 1, nkd_b1).
term(wg_b1, 1, slp).
term(wg_b1, 1, nkd_b2).
term(wg_b1, 1, ciact_b2).
term(wg_b1, 1, wg_b1).
term(wg_b1, 1, wg_b2).

%Regulators of wg_b2
edge(wg_b1, wg_b2, 1).
edge(slp, wg_b2, 1).
edge(en, wg_b2, 0).
edge(ciact_b1, wg_b2, 1).
edge(ciact_b2, wg_b2, 1).

%Regulatory function of wg_b2
function(wg_b2, 1).
term(wg_b2, 1, ciact_b1).
term(wg_b2, 1, ciact_b2).
term(wg_b2, 1, en).
term(wg_b2, 1, slp).
term(wg_b2, 1, wg_b1).

%Regulators of wg_ext
edge(wg_ext, wg_ext, 1).

%Regulatory function of wg_ext
function(wg_ext, 1).
term(wg_ext, 1, wg_ext).

