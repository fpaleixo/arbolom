%Compounds
compound(v1).
compound(v2).
compound(v3).
compound(v4).

%Regulators of v1
regulates(v2, v1, 0).

%Regulatory function of v1
function(v1, 1).
term(v1, 1, v2).

%Regulators of v2
regulates(v1, v2, 1).
regulates(v4, v2, 0).

%Regulatory function of v2
function(v2, 1).
term(v2, 1, v1).
term(v2, 1, v4).

%Regulators of v3
regulates(v1, v3, 0).
regulates(v2, v3, 0).
regulates(v4, v3, 1).

%Regulatory function of v3
function(v3, 2).
term(v3, 1, v1).
term(v3, 2, v2).
term(v3, 2, v4).

%Regulators of v4
regulates(v4, v4, 0).

%Regulatory function of v4
function(v4, 1).
term(v4, 1, v4).

