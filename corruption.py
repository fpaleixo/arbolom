import os
import sys
import glob
import random

path= './simple_models/'


#Receives a list of implicants as input. Returns a list of prime implicants.
def primesOnly(implicants):
  original = implicants.copy()
  copy = [set(i.strip("()").split('&')) for i in implicants] 
  #print("Processed input" + str(copy))

  output = []
  changed_input = []

  for i in range(0, len(implicants)):
    if(copy[i]==''): continue #if i has already been marked as a non-prime, go to the next implicant

    for j in range(i+1, len(implicants)):
      if(copy[j]==''): continue #if j has already been marked as a non-prime, go to the next implicant

      if copy[i].issubset(copy[j]): #if j absorbs i, then j is not a prime implicant
        changed_input.append(original[j])
        copy[j] = ''
      elif copy[j].issubset(copy[i]): #if j is absorbed by i, then i is not a prime implicant
        changed_input.append(original[i])
        copy[i] = ''
        break; #leave inner loop if i has absorbed another implicant
    
    if(copy[i] != ''): #if i has not absorbed any other implicant, it is a prime so add it to output
      output.append(original[i]) 

  return (changed_input, output)
        

#Receives a list of implicants as input, and the chance of removing an edge (regulator).
#A (repeated) literal in an implicant represents a signed edge (regulator). For all literals, roll the die 
#and see if the respective edge is removed or not.
def edgeRemove(implicants, chance):
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
      #print("Removing regulator "+l)
      changed_input.append(l)

      for i in range(0, len(implicants)): #For each implicant

        replaced = output[i].replace("&"+l, '') #Start by seeing if literal to remove is the last term of a conjunction
        if(replaced == output[i]):
          replaced = output[i].replace(l+"&", '') #If it wasn't, then check to see if it is the first term of a conjunction
          if(replaced == output[i]):
            replaced = output[i].replace(l, '') #If it is neither, then the literal occurs alone and can be removed without leaving behind a trailing &
        output[i] = replaced

  output = primesOnly(output)[1]
  return (changed_input, output)

#Receives a list of implicants as input, and the chance of changing an edge's sign.
#A (repeated) literal in an implicant represents a signed edge. For all literals, roll the die 
#and see if the sign of the respective edge changes or not.
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

      removed_edges = edgeRemove(implicants, 0.5)
      if(len(removed_edges[0]) > 0):
        print(">Removed edges from "+str(removed_edges[0])+" to "+ full[0] + ". New implicants: "+str(removed_edges[1]))
      else:
        print("No edges removed")

      flipped_implicants = edgeFlip(implicants, 0.1)
      if(len(flipped_implicants[0]) > 0):
        print(">Flipped literals "+str(flipped_implicants[0])+". New implicants: "+str(flipped_implicants[1]))
      else:
        print("No signs flipped")

    