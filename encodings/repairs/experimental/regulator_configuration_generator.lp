%Generates all possible regulator combinations

%Number of compounds in the model's universe
{chosen_compound_number(1..8)} = 1.

{variable(C) : node(C)} = NUMBER :- chosen_compound_number(NUMBER).

#show variable/1.
#show chosen_compound_number/1.