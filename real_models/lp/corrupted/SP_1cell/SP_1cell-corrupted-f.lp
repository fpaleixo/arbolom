%Compounds
compound(ci1).
compound(ciact_b1).
compound(ciact_b2).
compound(cirep).
compound(dsh).
compound(en).
compound(fz).
compound(hh).
compound(hh_ext).
compound(nkd_b1).
compound(nkd_b2).
compound(pka_b1).
compound(pka_b2).
compound(ptc_b1).
compound(ptc_b2).
compound(slp).
compound(wg_b1).
compound(wg_b2).
compound(wg_ext).

%Regulators of ci1
regulates(en, ci1, 1).

%Regulatory function of ci1
function(ci1, 1).
term(ci1, 1, en).

%Regulators of ciact_b1
regulates(ci1, ciact_b1, 0).
regulates(ciact_b1, ciact_b1, 0).
regulates(ciact_b2, ciact_b1, 0).
regulates(dsh, ciact_b1, 0).
regulates(pka_b1, ciact_b1, 1).

%Regulatory function of ciact_b1
function(ciact_b1, 2).
term(ciact_b1, 1, ci1).
term(ciact_b1, 1, ciact_b1).
term(ciact_b1, 1, ciact_b2).
term(ciact_b1, 1, dsh).
term(ciact_b1, 2, ci1).
term(ciact_b1, 2, ciact_b1).
term(ciact_b1, 2, dsh).
term(ciact_b1, 2, pka_b1).

%Regulators of ciact_b2
regulates(ci1, ciact_b2, 0).
regulates(pka_b1, ciact_b2, 1).
regulates(dsh, ciact_b2, 0).
regulates(ciact_b1, ciact_b2, 0).

%Regulatory function of ciact_b2
function(ciact_b2, 2).
term(ciact_b2, 1, ci1).
term(ciact_b2, 1, pka_b1).
term(ciact_b2, 2, ciact_b1).
term(ciact_b2, 2, dsh).
term(ciact_b2, 2, pka_b1).

%Regulators of cirep
regulates(dsh, cirep, 1).
regulates(ci1, cirep, 0).
regulates(pka_b2, cirep, 0).
regulates(pka_b1, cirep, 0).

%Regulatory function of cirep
function(cirep, 3).
term(cirep, 1, ci1).
term(cirep, 1, dsh).
term(cirep, 2, dsh).
term(cirep, 2, pka_b2).
term(cirep, 3, pka_b1).

%Regulators of dsh
regulates(fz, dsh, 0).

%Regulatory function of dsh
function(dsh, 1).
term(dsh, 1, fz).

%Regulators of en
regulates(slp, en, 1).
regulates(dsh, en, 0).

%Regulatory function of en
function(en, 2).
term(en, 1, slp).
term(en, 2, dsh).

%Regulators of fz
regulates(wg_b1, fz, 0).
regulates(wg_ext, fz, 0).

%Regulatory function of fz
function(fz, 2).
term(fz, 1, wg_b1).
term(fz, 2, wg_ext).

%Regulators of hh
regulates(cirep, hh, 1).
regulates(en, hh, 0).

%Regulatory function of hh
function(hh, 2).
term(hh, 1, cirep).
term(hh, 2, en).

%Regulators of hh_ext
regulates(hh_ext, hh_ext, 0).

%Regulatory function of hh_ext
function(hh_ext, 1).
term(hh_ext, 1, hh_ext).

%Regulators of nkd_b1
regulates(nkd_b1, nkd_b1, 0).
regulates(nkd_b2, nkd_b1, 0).
regulates(en, nkd_b1, 1).

%Regulatory function of nkd_b1
function(nkd_b1, 2).
term(nkd_b1, 1, nkd_b1).
term(nkd_b1, 1, nkd_b2).
term(nkd_b1, 2, en).

%Regulators of nkd_b2
regulates(dsh, nkd_b2, 0).
regulates(nkd_b1, nkd_b2, 0).
regulates(en, nkd_b2, 1).

%Regulatory function of nkd_b2
function(nkd_b2, 2).
term(nkd_b2, 1, dsh).
term(nkd_b2, 2, en).
term(nkd_b2, 2, nkd_b1).

%Regulators of pka_b1
regulates(pka_b1, pka_b1, 0).
regulates(pka_b2, pka_b1, 0).
regulates(ptc_b1, pka_b1, 0).

%Regulatory function of pka_b1
function(pka_b1, 2).
term(pka_b1, 1, pka_b1).
term(pka_b1, 2, pka_b2).
term(pka_b1, 2, ptc_b1).

%Regulators of pka_b2
regulates(pka_b1, pka_b2, 0).
regulates(ptc_b1, pka_b2, 0).

%Regulatory function of pka_b2
function(pka_b2, 2).
term(pka_b2, 1, pka_b1).
term(pka_b2, 2, ptc_b1).

%Regulators of ptc_b1
regulates(hh_ext, ptc_b1, 1).
regulates(en, ptc_b1, 1).
regulates(ptc_b1, ptc_b1, 0).
regulates(ptc_b2, ptc_b1, 0).

%Regulatory function of ptc_b1
function(ptc_b1, 2).
term(ptc_b1, 1, hh_ext).
term(ptc_b1, 2, en).
term(ptc_b1, 2, ptc_b1).
term(ptc_b1, 2, ptc_b2).

%Regulators of ptc_b2
regulates(en, ptc_b2, 1).
regulates(hh_ext, ptc_b2, 1).
regulates(ciact_b1, ptc_b2, 0).
regulates(ptc_b1, ptc_b2, 0).

%Regulatory function of ptc_b2
function(ptc_b2, 3).
term(ptc_b2, 1, en).
term(ptc_b2, 1, hh_ext).
term(ptc_b2, 2, ciact_b1).
term(ptc_b2, 3, hh_ext).
term(ptc_b2, 3, ptc_b1).

%Regulators of slp
regulates(en, slp, 1).
regulates(dsh, slp, 0).

%Regulatory function of slp
function(slp, 2).
term(slp, 1, en).
term(slp, 2, dsh).

%Regulators of wg_b1
regulates(nkd_b1, wg_b1, 1).
regulates(wg_b1, wg_b1, 0).
regulates(slp, wg_b1, 0).
regulates(en, wg_b1, 1).
regulates(ciact_b1, wg_b1, 0).
regulates(nkd_b2, wg_b1, 1).
regulates(ciact_b2, wg_b1, 0).
regulates(wg_b2, wg_b1, 0).

%Regulatory function of wg_b1
function(wg_b1, 3).
term(wg_b1, 1, nkd_b1).
term(wg_b1, 2, wg_b1).
term(wg_b1, 3, ciact_b1).
term(wg_b1, 3, ciact_b2).
term(wg_b1, 3, en).
term(wg_b1, 3, nkd_b2).
term(wg_b1, 3, slp).
term(wg_b1, 3, wg_b2).

%Regulators of wg_b2
regulates(en, wg_b2, 1).
regulates(slp, wg_b2, 0).
regulates(ciact_b1, wg_b2, 0).
regulates(ciact_b2, wg_b2, 0).
regulates(wg_b1, wg_b2, 0).

%Regulatory function of wg_b2
function(wg_b2, 3).
term(wg_b2, 1, en).
term(wg_b2, 2, ciact_b1).
term(wg_b2, 2, ciact_b2).
term(wg_b2, 2, slp).
term(wg_b2, 3, wg_b1).

%Regulators of wg_ext
regulates(wg_ext, wg_ext, 0).

%Regulatory function of wg_ext
function(wg_ext, 1).
term(wg_ext, 1, wg_ext).

