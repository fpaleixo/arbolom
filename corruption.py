import os
import sys
import glob
import random

path= './simple_models/'

#Auxiliary functions

#Takes a list of implicants as input, and outputs a  
#list containing all the literals in said implicant list (ex: v1 and !v1 are both present)
def getAllLiterals(implicants):

  #print(implicants)
  all_literals = [i.strip("()").split('&') for i in implicants]
  #print(all_literals)
  flatten_literals = [item for sublist in all_literals for item in sublist]
  #print(flatten_literals)
  literals = list(dict.fromkeys(flatten_literals))
  #print(literals)

  return literals


#Takes a dictionary containing all regulatory functions and returns a list with  
#all the compounds in them (ex: if both v1 and !v1 exist, only v1 is present)
def getAllCompounds(func_dict, add_self=True):

  implicant_list = list(func_dict.values())
  all_implicants = []

  for i in implicant_list:
      all_implicants += i
  #print(all_implicants)

  all_literals = getAllLiterals(all_implicants)

  #Adds the compounds in the keys to the list of compounds. Sometimes this is undesirable, 
  #e.g. when we just want the regulators of a compound (if the compound does not regulate itself, 
  #we would be incorrectly adding it to the list without this flag)
  if(add_self): 
    for k in func_dict.keys():
      all_literals.append(k)

  all_compounds = set()

  for l in all_literals:
    all_compounds.add(l.replace('!',""))

  return sorted(all_compounds)


#Returns a list with all the compounds that are regulators of the given input compound,
#for a given list of implicants
def getRegulatorsOf(compound, implicants):

  print("Obtained implicants of "+compound+":" +str(implicants))

  if not implicants: #If the compound has no implicants
    return []

  current_dict = {compound : implicants}

  all_regulators = getAllCompounds(current_dict, False)

  return all_regulators


#TODO: return with the right format(tuple with first position as the changed compounds, second position the updated dictionary); check correctness(done?); clean up prints; optimize other corruptions with new functions
def edgeAdd(func_dict, chance):
  #For each compound, make a loop with
  #each other compound that is not its regulator,
  #then roll the dice (given chance) and see if it is added as regulator (50% chance of being activator / inhibitor) or not
  #if it is added as a regulator, then roll the dice to see if it is added as an OR clause or 
  #added to one of the existing AND clauses (50%)
  #if it is added to one of the existing AND clauses, for each clause there's a 50% chance it will be included there

  all_compounds = getAllCompounds(func_dict)

  final_dict = {}

  for c in all_compounds:
    c_implicants = func_dict.get(c,[])
    c_regulators = getRegulatorsOf(c,c_implicants)
    
    #print("Regulators of "+c+" are: "+str(c_regulators))

    s = set(c_regulators)
    #Edges to be added need to come from compounds that are not regulators of c already
    potential_edges = [compound for compound in all_compounds if compound not in c_regulators]

    for e in potential_edges:
      roll = random.random()
      if(roll <= chance):
        print("Adding "+e+" as regulator of "+ c)

        roll = random.random()
        if(roll <=0.5): #Roll to see if e is activator or inhibitor
          print(e + " is going to be an inhibitor")
          e = '!'+e

        or_clause = True  
        roll = random.random()
        if(roll <=0.5):
          or_clause = False

        if(or_clause or not c_implicants):
          print("Adding "+e+ " as new prime implicant")
          c_implicants.append(e)

        else:
          print("Adding "+e+ " to existing prime implicant(s)")
          has_been_added = False
          for implicant in range (0, len(c_implicants)):
            roll = random.random()
            if(roll <=0.5 or (not has_been_added and implicant==len(c_implicants)-1)):
              print("adding it to implicant "+c_implicants[implicant])
              c_implicants[implicant]+='&'+e
              has_been_added = True

        print("Updated implicants: " + str(c_implicants))

  print(all_compounds)

  return 0

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
    print("(FILE) Reading file: " + filename)

    lines = [line.strip() for line in f.readlines()]
    func_dict = {}
    
    for regfun in lines:
      full = [c.strip() for c in regfun.split(',')]
      print("(READ) Read function: "+str(full))

      implicants = [i.replace(" ", "").strip("()") for i in full[1].split('|')]
      print("(I) Implicants of "+full[0]+": "+str(implicants))

      func_dict[full[0]] = implicants  #each compound is a key; the value is the corresponding list of prime implicants

      # removed_edges = edgeRemove(implicants, 0.5)
      # if(len(removed_edges[0]) > 0):
      #   print(">Removed edges from "+str(removed_edges[0])+" to "+ full[0] + ". New implicants: "+str(removed_edges[1]))
      # else:
      #   print("No edges removed")

      # flipped_implicants = edgeFlip(implicants, 0.1)
      # if(len(flipped_implicants[0]) > 0):
      #   print(">Flipped literals "+str(flipped_implicants[0])+". New implicants: "+str(flipped_implicants[1]))
      # else:
      #   print("No signs flipped")
    
    print("(READ END) Reached EOF")
    added_edges = edgeAdd(func_dict, 0.2)

    