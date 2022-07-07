import os, sys, argparse, logging, glob, random, re
from aux_scripts.common import *

#Usage: $python corruption.py -f (FILENAME) -op (OPERATIONS) -(O)p (PROBABILITY) -s (SAVE_DIRECTORY)

#Optional flags:
#-op -> Specify which corruptions to apply (default applies all corruptions).
#-(O)p -> Probability (0.0 to 1.0) of corruption O taking place (default is 0.2).
#-s -> Path of directory to save corrupted file 
# (default is ./simple_models/corrupted/(name_of_file)).

#Variables: 
#FILENAME -> Path of file inside simple models folder to corrupt.
#OPERATIONS -> A string with one (or more) specific characters, denoting which 
# corruptions to apply. These characters are 'f','e','r' and 'a'. 'fera' 
# would be the full string, representing that (f)unction change, (e)dge flip,
# edge (r)emove and edge (a)dd will all be applied.
#O -> A character that can take one of four possible values: 
# 'f','e','r' and 'a' (followed by 'p'). -fp would change the probability of 
# function change to occur, -ep of edge removal, etc. The argument that uses 
# this O variable is an optional one.
#PROBABILITY -> A float from 0.0 to 1.0 denoting the probability of a given 
# corruption to occur. For example, -ap 0.5 would change the add edge 
# operation's probability to 50%.
#SAVE_DIRECTORY -> Path of directory to save corrupted model to.

#Attention: 
# Input files must be in the BCF format and follow the conventions of 
# the .bnet files in the simple_models folder 
# (results will be unpredictable otherwise)


#-----Configs-----

#Command-line usage
cmd_enabled = True

#Original model paths
read_folder = './simple_models/'
filename = '6.bnet'

#Save path
write_folder = './simple_models/corrupted'

#Operations (set desired operations to True)
f_toggle = True #Function Change
e_toggle = True #Edge Sign Flip
r_toggle = True #Edge Remove
a_toggle = True #Edge Add

#Chances (probability that corruptions will occur (when set to True), 0 being 0% probability and 1 being 100%)
f_chance = 0.2
e_chance = 0.2
r_chance = 0.2
a_chance = 0.2

#Parser (will only be used if command-line usage is enabled above)
parser = None
args = None
if(cmd_enabled):
  parser = argparse.ArgumentParser(description=
    "Corrupt a Boolean logical model written in the BCF format.")
  parser.add_argument("-f", 
    "--file_to_corrupt", help="Path to file to be corrupted.")
  parser.add_argument("-op", 
    "--operations", help="Corruptions to apply.")
  parser.add_argument("-fp", 
    "--f_probability", help="Probability of applying function change.", 
    type=float)
  parser.add_argument("-ep", 
    "--e_probability", help="Probability of applying edge flip.", 
    type=float)
  parser.add_argument("-rp", 
    "--r_probability", help="Probability of applying edge remove.", 
    type=float)
  parser.add_argument("-ap", 
    "--a_probability", help="Probability of applying edge add.", 
    type=float)
  parser.add_argument("-s", 
  "--save_directory", help="Path of directory to save converted model to.")
  args = parser.parse_args()

#Global logger (change logging.(LEVEL) to desired (LEVEL) )
logging.basicConfig()
global_logger = logging.getLogger("global")
global_logger.setLevel(logging.INFO)

#Random seed (seed can be manually fixed to replicate results)
seed = random.randrange(sys.maxsize)
rng = random.Random(seed)
global_logger.info("Seed: "+ str(seed))



#-----Auxiliary functions-----

#Inputs: Receives a list of implicants.
#Purpose:  Returns a list of its prime implicants.
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
    #if i has already been marked as a non-prime or 
    #is already in the output, go to the next implicant
    if(copy[i]=='' or original[i] in output): continue 

    for j in range(i+1, orig_len):
      #if j has already been marked as a non-prime, go to the next implicant
      if(copy[j]==''): continue 

      #if j absorbs i, then j is not a prime implicant
      if copy[i].issubset(copy[j]): 
        changed_input.append(original[j])
        copy[j] = ''

      #if j is absorbed by i, then i is not a prime implicant
      elif copy[j].issubset(copy[i]): 
        changed_input.append(original[i])
        copy[i] = ''
        break; #leave inner loop if i has absorbed another implicant
    
    #if i has not absorbed any other implicant, it is a prime so add it to output
    if(copy[i] != ''): 
      output.append(original[i]) 

  return (changed_input, output)


#Input: A list of prime implicants, a list of literals that should be present 
# in the prime implicants.
#Purpose: If there are literals missing from the list of prime implicants, 
# add a new implicant with them.
def checkLiterals(implicants, literals):
  logger = logging.getLogger("check_literals")
  logger.setLevel(logging.INFO)
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


#Purpose: Parses the arguments for which operations are to be applied and 
# their probabilities.
def parseArgs():
  logger = logging.getLogger("parser")
  logger.setLevel(logging.INFO)

  filepath = args.file_to_corrupt
  operations = args.operations
  f_p = args.f_probability
  e_p = args.e_probability
  r_p = args.r_probability
  a_p = args.a_probability

  global read_folder, write_folder, filename 
  global f_toggle, e_toggle, r_toggle, a_toggle 
  global f_chance, e_chance, r_chance, a_chance

  if filepath:
    filename = os.path.basename(filepath)
    read_folder = os.path.dirname(filepath)
    write_folder = read_folder

  logger.debug("Filename is: "+ filename)
  logger.debug("Read folder is: "+ read_folder)

  if(args.save_directory):
    write_folder = args.save_directory
    logger.debug("Write folder is: "+ write_folder)

  if operations:
    if 'f' in operations:
      f_toggle = True
      if f_p:
        f_chance = f_p
    
    if 'e' in operations:
      e_toggle = True
      if e_p:
        e_chance = e_p

    if 'r' in operations:
      r_toggle = True
      if r_p:
        r_chance = r_p

    if 'a' in operations:
      a_toggle = True
      if a_p:
        a_chance = a_p

    logger.debug("Obtained operations: " + operations)

  logger.debug("Corruption F: "+ str(f_toggle) + " with chance " + str(f_chance))
  logger.debug("Corruption E: "+ str(e_toggle) + " with chance " + str(e_chance))
  logger.debug("Corruption R: "+ str(r_toggle) + " with chance " + str(r_chance))
  logger.debug("Corruption A: "+ str(a_toggle) + " with chance " + str(a_chance))
  
  return


#Input: dict is a dictionary with all the regulatory functions, path is 
# the folder where the file will be stored and file is the file name.
#Purpose: Stores the contents of the dictionary into a file using the
# .bnet format.
def saveToFile(dict, ops=''):
  logger = logging.getLogger("saveLP")
  logger.setLevel(logging.INFO)

  global read_folder, write_folder

  
  name = filename

  print("PATH IS: " + write_folder)
  print("NAME IS: " + name)
  current_path = uniquify(os.path.join(write_folder,
  name.replace(".bnet", '') + "-corrupted" + "-" + ops + ".bnet"))

  if not os.path.exists(os.path.dirname(current_path)):
    os.makedirs(os.path.dirname(current_path))
    logger.info("Created directory: " + str(os.path.dirname(current_path)))

  f = open(current_path, 'w')

  for function in dict.items():
    implicants = ''

    for i in function[1]:
      is_conjunction = '&' in i 

      if i == function[1][-1]: #If it is the last prime implicant
        if is_conjunction:
          implicants += "(" + i + ")" 
        else:
          implicants += i

      else:
        if is_conjunction:
          implicants += "(" + i + ") | "

        else:
          implicants += i + " | "

    f.write(function[0] + ", " + implicants + '\n')



#-----Model corruption operations-----
#Inputs: Receives a list of implicants as input, and the chance to change 
# that list of implicants (0.0-1.0).
#Purpose: Changes the regulatory function of a compound by creating a new one 
# using the same literals.
def funcChange(implicants, chance):
  logger = logging.getLogger("func_change")
  logger.setLevel(logging.INFO)

  output = None
  changed = False
  literals = getAllLiterals(implicants)

  logger.debug("Length of literals: "+ str(len(literals)))
  roll = rng.random()
  if(len(literals) > 1 and roll <= chance):
    changed = True

    num_implicants = rng.randint(1, 2*len(literals))
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
        roll = rng.random()

        if(roll <=0.5 
           #Literal has not been used yet and we're on the last possible 
           # implicant that it can be used in
           or (i==num_implicants-1 and not has_been_used) 
           #We're on the last literal and there is a clause that does not have 
           # any literals in it yet
           or (l==literals[-1] and i not in filled_clauses)): 
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
#that a new regulator will be added to the regulatory function of a compound.
#Purpose: Add more regulators to the regulatory function of a compound.
#Detail: For each compound, make a loop with
# each other compound that is not its regulator,
# then roll the dice (input chance) and see if it is added as 
# regulator (50% chance of being activator / inhibitor) or not.
# If it is added as a regulator, then roll the dice to see if it is added as 
# an OR clause or added to one of the existing AND clauses (50% chance).
# If it is added to one of the existing AND clauses, for each clause there's 
# a 50% chance it will be included there.
def edgeAdd(func_dict, chance):
  logger = logging.getLogger("edge_add")
  logger.setLevel(logging.INFO)

  all_compounds = getAllCompounds(func_dict)
  changed = set()

  final_dict = dict.fromkeys(func_dict.keys(),[]) #original keys are copied to preserve key ordering

  for c in all_compounds:
    c_implicants = func_dict.get(c,[])
    c_regulators = getRegulatorsOf(c,c_implicants)
    
    logger.debug("Regulators of "+c+" are: "+str(c_regulators))

    s = set(c_regulators)
    #Edges to be added need to come from compounds that are not regulators of c already
    potential_edges = [compound for compound in all_compounds if compound not in c_regulators]

    for e in potential_edges:
      roll = rng.random()
      if(roll <= chance/len(potential_edges)):
        logger.debug("Adding "+e+" as regulator of "+ c)
        changed.add(c)

        roll = rng.random()
        if(roll <=0.5): #Roll to see if e is activator or inhibitor
          logger.debug(e + " is going to be an inhibitor")
          e = '!'+e

        or_clause = True  
        roll = rng.random()
        if(roll <=0.5):
          or_clause = False

        if(or_clause or not c_implicants):
          logger.debug("Adding "+e+ " as new prime implicant")
          c_implicants.append(e)

        else:
          logger.debug("Adding "+e+" to existing prime implicant(s)")
          has_been_added = False

          for implicant in range (0, len(c_implicants)):
            roll = rng.random()

            if(roll <=0.5 or (not has_been_added and implicant==len(c_implicants)-1)):
              logger.debug("Adding it to implicant "+c_implicants[implicant])
              c_implicants[implicant]+='&'+e
              has_been_added = True

        logger.debug("Updated implicants: " + str(c_implicants))

    final_dict[c] = c_implicants

  logger.debug("Final dict: " + str(final_dict))

  return (changed, final_dict)


#Inputs: A list of implicants, and the chance of removing an edge (regulator).
#Purpose: For all literals in a regulatory function, roll the die and see 
# if the respective edge is removed or not.
def edgeRemove(implicants, chance):
  logger = logging.getLogger("edge_remove")
  logger.setLevel(logging.INFO)

  output = implicants.copy()
  changed_input = []

  literals = getAllLiterals(implicants)

  for l in literals:
    roll = rng.random()
    logger.debug("Rolled: " + str(roll))

    if(roll <= chance):
      logger.debug("Removing regulator " + l)
      changed_input.append(l)

      for i in range(0, len(implicants)): #For each implicant

        #Start by seeing if literal to remove is one of the middle terms in 
        # the conjunction
        replaced = output[i].replace("&" + l + "&", '&') 
        if replaced == output[i]: 
          #If it wasn't, then check if the literal to remove is the last term 
          # of a conjunction
          replaced = re.sub(r'&{}\b'.format(l), '', output[i]) 
          if replaced == output[i]:
            #If it wasn't, then check to see if it is the first term of 
            # a conjunction
            replaced = output[i].replace(l + "&", '') 
            if(replaced == output[i]):
              #If it is neither, then the literal occurs alone and can 
              # be removed without leaving behind a trailing '&'
              replaced = re.sub(r'\b{}\b'.format(l), '', output[i]) 
        output[i] = replaced

  output = primesOnly(output)[1]
  return (changed_input, output)


#Inputs: A list of implicants, and the chance of changing an edge's sign.
#Purpose: A (repeated) literal in an implicant represents a signed edge. 
# For all literals, roll the die and see if the sign of the respective 
# edge changes or not.
def edgeFlip(implicants, chance):
  logger = logging.getLogger("edge_flip")
  logger.setLevel(logging.INFO)

  output = implicants.copy()
  changed_input = []

  literals = getAllLiterals(implicants)

  for l in literals:
    roll = rng.random()
    logger.debug("Rolled: " + str(roll))

    if(roll <= chance):
      logger.debug("Changing sign of " + l)
      changed_input.append(l)
      negated = l.count('!')
      logger.debug("Negated yes/no? " + str(negated))

      if(negated%2 != 0): #if the literal is negated
        output = [re.sub(r'\b{}\b'.format('!'+l), l , i) for i in output]

      else:
        output = [re.sub(r'\b{}\b'.format(l), '!'+l , i) for i in output]
      
      logger.debug("Changed a sign: " + str(output))

  return (changed_input, output)



#-----Main-----

if(cmd_enabled):
  parseArgs()

for fname in glob.glob(os.path.join(read_folder, filename)):
  with open(os.path.join(os.getcwd(), fname), 'r') as f:
    global_logger.info("Reading file: " + filename)

    lines = [line.strip() for line in f.readlines()]
    func_dict = {}
    final_dict = {}

    f_effect = False
    e_effect = False
    r_effect = False
    a_effect = False
    
    for regfun in lines:
      full = [c.strip() for c in regfun.split(',')]
      global_logger.info("Read function: "+str(full))

      implicants = [i.replace(" ", "").strip("()") for i in full[1].split('|')]
      global_logger.debug("Implicants of "+full[0]+": "+str(implicants))

      #each compound is a key; the value is the corresponding list of prime implicants
      func_dict[full[0]] = implicants  

      if(f_toggle):
        change = funcChange(implicants, f_chance)

        if(change[0]):
          global_logger.info("("+full[0]+") " + "Changed reg func to " + str(change[1]))
          implicants = change[1]
          f_effect = True

        else:
          global_logger.info("("+full[0]+") " + "No changes to reg func")

      if(e_toggle):
        flipped_implicants = edgeFlip(implicants, e_chance)

        if(len(flipped_implicants[0]) > 0):
          global_logger.info("("+full[0]+") " + "Flipped literals " + 
            str(flipped_implicants[0]) + 
            ". New implicants: "+str(flipped_implicants[1]))
          implicants = flipped_implicants[1]
          e_effect = True

        else:
          global_logger.info("("+full[0]+") " + "No signs flipped")

      if(r_toggle):
        removed_edges = edgeRemove(implicants, r_chance)

        if(len(removed_edges[0]) > 0):
          global_logger.info("("+full[0]+") " + "Removed edges from " + 
           str(removed_edges[0]) + 
           ". New implicants: "+str(removed_edges[1]))
          implicants = removed_edges[1]
          r_effect = True

        else:
          global_logger.info("("+full[0]+") " + "No edges removed")

      final_dict[full[0]] = implicants #Update final corrupted model
    
    global_logger.info("Reached EOF")
    if(a_toggle):
      added_edges = edgeAdd(final_dict, a_chance)

      if(added_edges[0]):
        global_logger.info("Added new regulators to compound(s) " +
         str(added_edges[0]) + 
         ". New functions: "+str(added_edges[1]))
        final_dict = added_edges[1]
        a_effect = True
        
      else:
        global_logger.info("No edges added")

    #Operations that changed the model
    ops = ''
    if(f_effect):
      ops += 'f'
    if(e_effect):
      ops += 'e'
    if(r_effect):
      ops += 'r'
    if(a_effect):
      ops += 'a'  

    saveToFile(final_dict, ops=ops)