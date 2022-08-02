from aux_scripts.common import getAllLiterals, getRegulatorsOf

def getFunctionDict(lines, logger):
  func_dict = {}

  for regfun in lines:
    if regfun == '': #ignore blank lines
      continue
    else:
      full = [c.strip() for c in regfun.split(',')]
      if logger : logger.debug("Read function: "+str(full))

      implicants = [i.replace(" ", "").strip("()") for i in full[1].split('|')]
      if logger : logger.debug("Implicants of "+full[0]+": "+str(implicants))

      #each compound is a key; the value is the corresponding 
      # list of prime implicants
      func_dict[full[0]] = implicants  

  return func_dict

#Inputs: file is the file to write in, compounds is a list of strings 
# representing the compounds.
#Purpose: Adds predicates representing compounds to LP.
def addCompoundsToResult(string, compounds):
  string += "%Compounds\n"
  for c in compounds:
    string += "compound(" + c + ").\n"
  string +="\n"
  return string


#Inputs: file is the file to write in, item is a tuple where the first element 
# is the compound of the regulatory function, 
# and the second element is a list of its implicants.
#Purpose: Adds the predicates representing the regulators of each compound to LP.
def addRegulatorsToResult(string, item):
  if item[1][0]: #if there exist any regulators
    string += "%Regulators of " + item[0] + "\n"
    all_literals = getAllLiterals(item[1])

    for l in all_literals:
      if(l[0]=='!'):
        string += "regulates(" + l[1:] + ", " + item[0] + ", " + "1).\n"

      else:
        string += "regulates(" + l + ", " + item[0] + ", " + "0).\n"
    string += "\n"
  return string


#Inputs: file is the file to write in, item is a tuple where the first element 
# is the compound of the regulatory function, 
# and the second element is a list of its implicants.
#Purpose: Adds regulators of each compound to LP.
def addFunctionToResult(string, item):
  if item[1][0]: #if there exist any regulators
    string += "%Regulatory function of " + item[0] + "\n"
    num_terms = len(item[1])
    string += "function(" + item[0] + ", " + str(num_terms) + ").\n" 

    for idx, i in enumerate(item[1]):
      regulators = getRegulatorsOf(item[0],[i])
      
      for r in regulators:
        string += "term(" + item[0] + ", " + str(idx+1) + ", " + r + ").\n"

    string +="\n"
  return string