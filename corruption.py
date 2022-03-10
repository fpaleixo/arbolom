import os
import sys
import glob
import random

path= './simple_models/'


#Receives a list of implicants as input, and the chance of changing an edge's sign.
#A (repeated) literal in an implicant represents a signed edge. For all literals, roll the die 
#and see if the sign changes or not.
def edgeFlip(implicants, chance):
  output = implicants.copy()
  changed_input = []

  #print(implicants)
  all_literals = [i.strip("()").split('&') for i in implicants]
  #print(all_literals)
  flatten_literals = [item for sublist in all_literals for item in sublist]
  #print(flatten_literals)
  literals = list(dict.fromkeys(flatten_literals))
  #print(literals)

  for l in literals:
    roll = random.random()
    #print("Rolled: " + str(roll))
    if(roll <= chance):
      #print("Changing sign of "+l)
      changed_input.append(l)
      negated = l.count('!')
      #print(negated)

      if(negated%2 != 0): #if the literal is negated
        output = [i.replace(l, l.replace('!','')) for i in output]
      else:
        output = [i.replace(l, "!"+l) for i in output]
        #print("Check it out: " + str(output))

  return (changed_input, output)
        


for filename in glob.glob(os.path.join(path, '8.bnet')):
  with open(os.path.join(os.getcwd(), filename), 'r') as f:
    print(filename)

    lines = [s.strip() for s in f.readlines()]
    
    for regfun in lines:
      full = regfun.split(',')
      print("Full function: "+str(full))
      implicants = [i.replace(" ", "") for i in full[1].split('|')]
      print("Implicants "+full[0]+": "+str(implicants))
      flipped_implicants = edgeFlip(implicants, 0.1)
      if(len(flipped_implicants[0]) > 0):
        print(" Flipped literals "+str(flipped_implicants[0])+": "+str(flipped_implicants[1]))
      else:
        print("No change")

    