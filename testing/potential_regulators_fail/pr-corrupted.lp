%Compounds
compound(a).
compound(b).
compound(c).

%Regulators of a
regulates(b, a, 1).
fixed(b,a,1).

%Regulatory function of a
function(a, 1).
term(a, 1, b).

%Regulators of b
regulates(b, b, 0).

%Regulatory function of b
function(b, 1).
term(b, 1, b).

%Regulators of c
regulates(c, c, 1).

%Regulatory function of c
function(c, 1).
term(c, 1, c).

