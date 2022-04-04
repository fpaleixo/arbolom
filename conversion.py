import os, argparse, logging, glob
from aux_scripts.common import *

#Usage: $python conversion.py -f (FILENAME) -s (SAVE_DIRECTORY)
#Optional flags:
#-s -> Path of directory to save converted file (default is ./lp_models/corrupted/(name_of_file))
#Variables: 
#FILENAME -> Path of file containing Boolean model in the BCF format to convert to ASP.
#SAVE_DIRECTORY -> Path of directory to save converted model to.

#Attention: Input files must be in the BCF format and follow the conventions of the .bnet files in the simple_models folder (results will be unpredictable otherwise)

#-----Configs-----

#Command-line usage
cmd_enabled = True

#Original model paths
read_folder= './simple_models/'
write_folder= './lp_models/corrupted'
filename = '5.bnet'

#Parser (will only be used if command-line usage is enabled above)
parser = None
args = None
if(cmd_enabled):
  parser = argparse.ArgumentParser(description="Convert a Boolean logical model written in the BCF format to a logic program.")
  parser.add_argument("-f", "--file_to_convert", help="Path to file to be converted.")
  parser.add_argument("-s", "--save_directory", help="Path of directory to save converted model to.")
  args = parser.parse_args()

#Global logger (change logging.(LEVEL) to desired (LEVEL) )
logging.basicConfig()
global_logger = logging.getLogger("global")
global_logger.setLevel(logging.DEBUG)



#-----Auxiliary functions-----

#Purpose: Parses the argument regarding which file to convert.
def parseArgs():
  logger = logging.getLogger("parser")
  logger.setLevel(logging.DEBUG)

  global read_folder, write_folder, filename

  filepath = args.file_to_convert

  filename = os.path.basename(filepath)
  read_folder = os.path.dirname(filepath)

  if(args.save_directory):
    write_folder = args.save_directory

  logger.debug("Obtained file: " + filepath)
  logger.debug("Name: " + filename)
  logger.debug("Directory: " + read_folder)
  return



#-----ASP Predicates-related operations-----

#Inputs: file is the file to write in, compounds is a list of strings representing the compounds.
#Purpose: Adds nodes representing compounds to LP
def addNodesToLP(file, compounds):
  file.write("%Compounds\n")
  for c in compounds:
    file.write("node(" + c + ").\n")
  file.write("\n")


#Inputs: file is the file to write in, item is a tuple where the first element is the compound of the regulatory function, and the second element is a list of its implicants.
#Purpose: Adds the edges representing the regulators of each node to LP
def addEdgesToLP(file, item):
  if item[1][0]: #if there exist any regulators
    file.write("%Regulators of " + item[0] + "\n")
    all_literals = getAllLiterals(item[1])

    for l in all_literals:
      if(l[0]=='!'):
        file.write("edge(" + l[1:] + ", " + item[0] + ", " + "1).\n")

      else:
        file.write("edge(" + l + ", " + item[0] + ", " + "0).\n")
    file.write("\n")


#Inputs: file is the file to write in, item is a tuple where the first element is the compound of the regulatory function, and the second element is a list of its implicants.
#Purpose: Adds regulators of each compound to LP
def addFunctionToLP(file, item):
  if item[1][0]: #if there exist any regulators
    file.write("%Regulatory function of " + item[0] + "\n")
    num_terms = len(item[1])
    file.write("function(" + item[0] + ", " + str(num_terms) + ").\n") 

    for idx, i in enumerate(item[1]):
      regulators = getRegulatorsOf(item[0],[i])
      
      for r in regulators:
        file.write("term(" + item[0] + ", " + str(idx+1) + ", " + r + ").\n") #should we store the sign on the edges or on the function itself?

    file.write("\n")



#-----Convert to LP operations-----

#Inputs: dict is a dictionary where the keys are compounds and the values are the implicants of each compound, name is the name of the file and path is the directory to place the file in
#Purpose: Saves a Boolean logical model to an LP file
def saveLPToFile(dict, name=False, path=write_folder):
  logger = logging.getLogger("saveLP")
  logger.setLevel(logging.DEBUG)

  if not name:
    name = filename

  logger.debug("Filename: " + str(name))
  logger.debug("Path: " + str(write_folder))

  current_path = None
  if 'corrupted' in name and not args.save_directory:
    base_filename = name.split('-')[0] 
    current_path = os.path.join(path, base_filename, name.replace(".bnet", '.lp'))
  else:
    current_path = os.path.join(path, name.replace(".bnet", '.lp'))
  f = open(current_path, 'w')

  logger.debug("Saving to: " + str(current_path))
  
  all_compounds = getAllCompounds(dict, True)
  logger.debug("All compounds: " + str(all_compounds))

  if len(all_compounds) == len(list(dict.keys())):
    addNodesToLP(f, list(dict.keys())) #If all compounds are present in the map keys then the original order is preserved for convenience
  else: 
    addNodesToLP(f, all_compounds)  

  for function in dict.items():
    addEdgesToLP(f,function)
    addFunctionToLP(f,function)
  f.close()



#-----Main-----

if(cmd_enabled):
  parseArgs()

for fname in glob.glob(os.path.join(read_folder, filename)):
  with open(os.path.join(os.getcwd(), fname), 'r') as f:
    global_logger.info("Reading file: " + filename)

    lines = [line.strip() for line in f.readlines()]
    func_dict = {}
    
    for regfun in lines:
      full = [c.strip() for c in regfun.split(',')]
      global_logger.info("Read function: "+str(full))

      implicants = [i.replace(" ", "").strip("()") for i in full[1].split('|')]
      global_logger.debug("Implicants of "+full[0]+": "+str(implicants))

      func_dict[full[0]] = implicants  #each compound is a key; the value is the corresponding list of prime implicants

    saveLPToFile(func_dict)

    