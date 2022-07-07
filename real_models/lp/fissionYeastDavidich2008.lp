%Compounds
compound(cdc25).
compound(cdc2_cdc13).
compound(cdc2_cdc13_a).
compound(pp).
compound(rum1).
compound(sk).
compound(slp1).
compound(start).
compound(ste9).
compound(wee1_mik1).

%Regulators of cdc25
regulates(cdc2_cdc13, cdc25, 1).
regulates(pp, cdc25, 0).
regulates(cdc25, cdc25, 1).

%Regulatory function of cdc25
function(cdc25, 3).
term(cdc25, 1, cdc2_cdc13).
term(cdc25, 1, pp).
term(cdc25, 2, cdc25).
term(cdc25, 2, pp).
term(cdc25, 3, cdc25).
term(cdc25, 3, cdc2_cdc13).

%Regulators of cdc2_cdc13
regulates(ste9, cdc2_cdc13, 0).
regulates(rum1, cdc2_cdc13, 0).
regulates(slp1, cdc2_cdc13, 0).

%Regulatory function of cdc2_cdc13
function(cdc2_cdc13, 1).
term(cdc2_cdc13, 1, rum1).
term(cdc2_cdc13, 1, slp1).
term(cdc2_cdc13, 1, ste9).

%Regulators of cdc2_cdc13_a
regulates(ste9, cdc2_cdc13_a, 0).
regulates(rum1, cdc2_cdc13_a, 0).
regulates(slp1, cdc2_cdc13_a, 0).
regulates(wee1_mik1, cdc2_cdc13_a, 0).
regulates(cdc25, cdc2_cdc13_a, 1).

%Regulatory function of cdc2_cdc13_a
function(cdc2_cdc13_a, 1).
term(cdc2_cdc13_a, 1, cdc25).
term(cdc2_cdc13_a, 1, rum1).
term(cdc2_cdc13_a, 1, slp1).
term(cdc2_cdc13_a, 1, ste9).
term(cdc2_cdc13_a, 1, wee1_mik1).

%Regulators of pp
regulates(slp1, pp, 1).

%Regulatory function of pp
function(pp, 1).
term(pp, 1, slp1).

%Regulators of rum1
regulates(cdc2_cdc13, rum1, 0).
regulates(cdc2_cdc13_a, rum1, 0).
regulates(rum1, rum1, 1).
regulates(sk, rum1, 0).
regulates(pp, rum1, 1).

%Regulatory function of rum1
function(rum1, 5).
term(rum1, 1, cdc2_cdc13).
term(rum1, 1, cdc2_cdc13_a).
term(rum1, 1, rum1).
term(rum1, 1, sk).
term(rum1, 2, cdc2_cdc13).
term(rum1, 2, cdc2_cdc13_a).
term(rum1, 2, pp).
term(rum1, 2, sk).
term(rum1, 3, cdc2_cdc13).
term(rum1, 3, cdc2_cdc13_a).
term(rum1, 3, pp).
term(rum1, 3, rum1).
term(rum1, 4, cdc2_cdc13).
term(rum1, 4, pp).
term(rum1, 4, rum1).
term(rum1, 4, sk).
term(rum1, 5, cdc2_cdc13_a).
term(rum1, 5, pp).
term(rum1, 5, rum1).
term(rum1, 5, sk).

%Regulators of sk
regulates(start, sk, 1).

%Regulatory function of sk
function(sk, 1).
term(sk, 1, start).

%Regulators of slp1
regulates(cdc2_cdc13_a, slp1, 1).

%Regulatory function of slp1
function(slp1, 1).
term(slp1, 1, cdc2_cdc13_a).

%Regulators of ste9
regulates(cdc2_cdc13, ste9, 0).
regulates(cdc2_cdc13_a, ste9, 0).
regulates(ste9, ste9, 1).
regulates(sk, ste9, 0).
regulates(pp, ste9, 1).

%Regulatory function of ste9
function(ste9, 5).
term(ste9, 1, cdc2_cdc13).
term(ste9, 1, cdc2_cdc13_a).
term(ste9, 1, sk).
term(ste9, 1, ste9).
term(ste9, 2, cdc2_cdc13).
term(ste9, 2, cdc2_cdc13_a).
term(ste9, 2, pp).
term(ste9, 2, sk).
term(ste9, 3, cdc2_cdc13).
term(ste9, 3, cdc2_cdc13_a).
term(ste9, 3, pp).
term(ste9, 3, ste9).
term(ste9, 4, cdc2_cdc13).
term(ste9, 4, pp).
term(ste9, 4, sk).
term(ste9, 4, ste9).
term(ste9, 5, cdc2_cdc13_a).
term(ste9, 5, pp).
term(ste9, 5, sk).
term(ste9, 5, ste9).

%Regulators of wee1_mik1
regulates(cdc2_cdc13, wee1_mik1, 0).
regulates(wee1_mik1, wee1_mik1, 1).
regulates(pp, wee1_mik1, 1).

%Regulatory function of wee1_mik1
function(wee1_mik1, 3).
term(wee1_mik1, 1, cdc2_cdc13).
term(wee1_mik1, 1, wee1_mik1).
term(wee1_mik1, 2, cdc2_cdc13).
term(wee1_mik1, 2, pp).
term(wee1_mik1, 3, pp).
term(wee1_mik1, 3, wee1_mik1).

