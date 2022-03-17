import os, sys, logging, glob, random
#TO-DO: 
#add acquirable seed; testing

#Config
global_logger = logging.getLogger("global")
global_logger.setLevel(logging.DEBUG)
path= './simple_models/'

#-----Auxiliary functions-----

#Inputs: A list of implicants
#Purpose: Outputs a list containing all the literals in said implicant list (ex: v1 and !v1 are both present)
def getAllLiterals(implicants):
  logger = logging.getLogger("all_literals")
  logger.setLevel(logging.INFO)

  logger.debug(implicants)
  all_literals = [i.strip("()").split('&') for i in implicants]
  
  logger.debug(all_literals)
  flatten_literals = [item for sublist in all_literals for item in sublist]

  logger.debug(flatten_literals)
  literals = list(dict.fromkeys(flatten_literals))
  
  logger.debug(literals)
  return literals


#Inputs: A dictionary containing all the regulatory functions and an optional argument to add the compound in the key
#Purpose: Outputs all the compounds in a regulatory function (ex: if both v1 and !v1 exist, only v1 is present)
def getAllCompounds(func_dict, add_self=True):
  logger = logging.getLogger("all_compounds")
  logger.setLevel(logging.INFO)

  implicant_list = list(func_dict.values())
  all_implicants = []

  for i in implicant_list:
      all_implicants += i
  logger.debug(all_implicants)

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


#Inputs: Takes a compound and the corresponding list of implicants
#Purpose: Returns a list with all the compounds that are regulators of the given input compound
def getRegulatorsOf(compound, implicants):
  logger = logging.getLogger("regulators_of")
  logger.setLevel(logging.INFO)

  logger.debug("Obtained implicants of "+compound+":" +str(implicants))

  if not implicants: #If the compound has no implicants
    return []

  current_dict = {compound : implicants}

  all_regulators = getAllCompounds(current_dict, False)

  return all_regulators


#Inputs: Receives a list of implicants
#Purpose:  Returns a list of its prime implicants
def primesOnly(implicants):
  logger = logging.getLogger("primes_only")
  logger.setLevel(logging.INFO)

  original = [i for i in implicants if(i != '')]
  orig_len = len(original)
  copy = [set(i.strip("()").split('&')) for i in implicants] 
  logger.debug("Processed input" + str(copy))

  output = []
  changed_input = []

  for i in range(0, orig_len):
    if(copy[i]==''): continue #if i has already been marked as a non-prime, go to the next implicant

    for j in range(i+1, orig_len):
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


#Input: A list of prime implicants, a list of literals that should be present in the prime implicants
#Purpose: If there are literals missing from the list of prime implicants, add a new implicant with them
def checkLiterals(implicants, literals):
  logger = logging.getLogger("check_literals")
  logger.setLevel(logging.DEBUG)
  output = implicants.copy()

  imp_literals = getAllLiterals(implicants)
  missing_literals_implicant = None

  logger.debug("Received implicants: " + str(implicants))
  for l in literals:
    if l not in imp_literals:
      logger.debug("Found literal not in primes: " + l)
      if not missing_literals_implicant:
        missing_literals_implicant = l
      else:
        missing_literals_implicant += '&' + l
  
  if(missing_literals_implicant):
    output.append(missing_literals_implicant)
  return output


#-----Model corruption operations-----

#Inputs: Receives a list of implicants as input, and the chance to change that list of implicants (0.0-1.0).
#Purpose: Changes the regulatory function of a compound by creating a new one using the same literals.
def funcChange(implicants, chance):
  logger = logging.getLogger("func_change")
  logger.setLevel(logging.DEBUG)

  output = None
  changed = False
  literals = getAllLiterals(implicants)

  roll = random.random()
  if(len(literals) > 1 and roll <=0.5):
    changed = True

    num_implicants = random.randint(1, 2*len(literals))
    if(num_implicants > len(literals)+1):
      logger.debug("Max implicants initial: " + str(num_implicants))
      num_implicants = round(num_implicants /2)+1

    logger.debug("Number of max implicants set: "+ str(num_implicants))

    output = [None]*num_implicants
    filled_clauses = {}

    for l in literals:
      logger.debug("Looking at literal "+l)
      has_been_used = False

      for i in range(0, num_implicants):
        roll = random.random()

        if(roll <=0.5 
           or (i==num_implicants-1 and not has_been_used) #Literal has not been used yet and we're on the last possible implicant that it can be used in
           or (l==literals[-1] and i not in filled_clauses)): #We're on the last literal and there is a clause that does not have any literals in it yet
          logger.debug("Adding it to clause "+ str(i+1))
          has_been_used = True
          filled_clauses[i] = True

          if(output[i] == None):
            output[i] = l
          else:
            output[i] += "&"+l
          logger.debug("Updated implicants: "+ str(output))

    output = checkLiterals(primesOnly(output)[1], literals)

  return (changed, output)


#Inputs: A dictionary containing all the regulatory functions and the chance 
#that a new regulator will be added to the regulatory function of a compound
#Purpose: Add more regulators to the regulatory function of a compound
#Detail: For each compound, make a loop with
#each other compound that is not its regulator,
#then roll the dice (given chance) and see if it is added as regulator (50% chance of being activator / inhibitor) or not
#if it is added as a regulator, then roll the dice to see if it is added as an OR clause or 
#added to one of the existing AND clauses (50%)
#if it is added to one of the existing AND clauses, for each clause there's a 50% chance it will be included there
def edgeAdd(func_dict, chance):
  logger = logging.getLogger("edge_add")
  logger.setLevel(logging.DEBUG)

  all_compounds = getAllCompounds(func_dict)
  changed = False

  final_dict = {}

  for c in all_compounds:
    c_implicants = func_dict.get(c,[])
    c_regulators = getRegulatorsOf(c,c_implicants)
    
    logger.debug("Regulators of "+c+" are: "+str(c_regulators))

    s = set(c_regulators)
    #Edges to be added need to come from compounds that are not regulators of c already
    potential_edges = [compound for compound in all_compounds if compound not in c_regulators]

    for e in potential_edges:
      roll = random.random()
      if(roll <= chance/len(potential_edges)):
        logger.debug("Adding "+e+" as regulator of "+ c)
        changed = True

        roll = random.random()
        if(roll <=0.5): #Roll to see if e is activator or inhibitor
          logger.debug(e + " is going to be an inhibitor")
          e = '!'+e

        or_clause = True  
        roll = random.random()
        if(roll <=0.5):
          or_clause = False

        if(or_clause or not c_implicants):
          logger.debug("Adding "+e+ " as new prime implicant")
          c_implicants.append(e)

        else:
          logger.debug("Adding "+e+" to existing prime implicant(s)")
          has_been_added = False
          for implicant in range (0, len(c_implicants)):
            roll = random.random()
            if(roll <=0.5 or (not has_been_added and implicant==len(c_implicants)-1)):
              logger.debug("Adding it to implicant "+c_implicants[implicant])
              c_implicants[implicant]+='&'+e
              has_been_added = True

        logger.debug("Updated implicants: " + str(c_implicants))
    if(c_implicants):
      final_dict[c] = c_implicants

  logger.debug("Final dict: " + str(final_dict))

  return (changed, final_dict)


#Inputs: A list of implicants, and the chance of removing an edge (regulator).
#Purpose: For all literals in a regulatory function, roll the die and see if the respective edge is removed or not.
def edgeRemove(implicants, chance):
  logger = logging.getLogger("edge_remove")
  logger.setLevel(logging.INFO)

  output = implicants.copy()
  changed_input = []

  literals = getAllLiterals(implicants)

  for l in literals:
    roll = random.random()
    logger.debug("Rolled: " + str(roll))
    if(roll <= chance):
      logger.debug("Removing regulator "+l)
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


#Inputs: A list of implicants, and the chance of changing an edge's sign
#Purpose: A (repeated) literal in an implicant represents a signed edge. For all literals, roll the die 
#and see if the sign of the respective edge changes or not.
def edgeFlip(implicants, chance):
  logger = logging.getLogger("edge_flip")
  logger.setLevel(logging.INFO)

  output = implicants.copy()
  changed_input = []

  literals = getAllLiterals(implicants)

  for l in literals:
    roll = random.random()
    logger.debug("Rolled: " + str(roll))
    if(roll <= chance):
      logger.debug("Changing sign of "+l)
      changed_input.append(l)
      negated = l.count('!')
      logger.debug(negated)

      if(negated%2 != 0): #if the literal is negated
        output = [i.replace(l, l.replace('!','')) for i in output]
      else:
        output = [i.replace(l, "!"+l) for i in output]
        logger.debug("Check it out: " + str(output))

  return (changed_input, output)


#-----Main-----
for filename in glob.glob(os.path.join(path, '8.bnet')):
  with open(os.path.join(os.getcwd(), filename), 'r') as f:
    global_logger.info("Reading file: " + filename)

    lines = [line.strip() for line in f.readlines()]
    func_dict = {}
    
    for regfun in lines:
      full = [c.strip() for c in regfun.split(',')]
      global_logger.info("Read function: "+str(full))

      implicants = [i.replace(" ", "").strip("()") for i in full[1].split('|')]
      global_logger.debug("Implicants of "+full[0]+": "+str(implicants))

      func_dict[full[0]] = implicants  #each compound is a key; the value is the corresponding list of prime implicants

      # removed_edges = edgeRemove(implicants, 0.5)
      # if(len(removed_edges[0]) > 0):
      #   global_logger.info("Removed edges from "+str(removed_edges[0])+" to "+ full[0] + ". New implicants: "+str(removed_edges[1]))
      # else:
      #   global_logger.info("No edges removed")

      # change = funcChange(implicants, 0.8)
      # if(change[0]):
      #   global_logger.info("Changed reg func of "+full[0]+" to " + str(change[1]))
      # else:
      #   global_logger.info("No change")

      # flipped_implicants = edgeFlip(implicants, 0.3)
      # if(len(flipped_implicants[0]) > 0):
      #   global_logger.info("Flipped literals "+str(flipped_implicants[0])+". New implicants: "+str(flipped_implicants[1]))
      # else:
      #   global_logger.info("No signs flipped")
    
    global_logger.info("(READ END) Reached EOF")
    added_edges = edgeAdd(func_dict, 0.2)
    if(added_edges[0]):
      global_logger.info("Added regulators to " + full[0] + ". New functions: "+str(added_edges[1]))
    else:
      global_logger.info("No changes")

    