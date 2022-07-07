%Compounds
compound(v1).
compound(v2).
compound(v3).

%Regulators of v1
regulates(v2, v1, 1).
regulates(v3, v1, 1).

%Regulatory function of v1
function(v1, 1).
term(v1, 1, v2).
term(v1, 1, v3).

%Regulators of v2
regulates(v3, v2, 0).

%Regulatory function of v2
function(v2, 1).
term(v2, 1, v3).

%Regulators of v3
regulates(v2, v3, 0).

%Regulatory function of v3
function(v3, 1).
term(v3, 1, v2).

