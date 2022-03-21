import os, logging

#-----Auxiliary functions called by more than one module-----

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



