import os, argparse, logging, glob
from aux_scripts.common import getAllCompounds
from aux_scripts.conversion_functions import *

#Usage: $python conversion.py -f (FILENAME) -s (SAVE_DIRECTORY)

#Optional flags:
#-s -> Path of directory to save converted file (default is ./lp_models/corrupted/(name_of_file))

#Variables: 
#FILENAME -> Path of file containing Boolean model in the BCF format to convert to ASP.
#SAVE_DIRECTORY -> Path of directory to save converted model to.

#Attention: 
# Input files must be in the BCF format and follow the conventions of 
# the .bnet files in the simple_models folder (results will be unpredictable otherwise)


#-----Configs-----
#Command-line usage
cmd_enabled = True

#Original model paths
read_folder = 'simple_models/'
write_folder = 'simple_models/lp/corrupted'
filename = '5.bnet'

#Parser (will only be used if command-line usage is enabled above)
parser = None
args = None
if(cmd_enabled):
  parser = argparse.ArgumentParser(description=
    "Convert a Boolean logical model written in the BCF format to a logic program.")
  parser.add_argument("-f", "--file_to_convert", help=
    "Path to file to be converted.")
  parser.add_argument("-s", "--save_directory", help=
    "Path of directory to save converted model to.")
  args = parser.parse_args()

#Global logger (change logging.(LEVEL) to desired (LEVEL) )
logging.basicConfig()
global_logger = logging.getLogger("global")
global_logger.setLevel(logging.INFO)



#-----Auxiliary functions-----

#Purpose: Parses the argument regarding which file to convert.
def parseArgs():
  logger = logging.getLogger("parser")
  logger.setLevel(logging.INFO)

  global read_folder, write_folder, filename

  filepath = args.file_to_convert

  filename = os.path.basename(filepath)
  read_folder = os.path.dirname(filepath)
  write_folder = read_folder

  if(args.save_directory):
    write_folder = args.save_directory

  logger.info("Obtained file: " + filepath)
  logger.debug("Name: " + filename)
  logger.debug("Directory: " + read_folder)
  return


#-----Convert to LP operations-----

#Inputs: 'dict' is a dictionary where the keys are compounds and the values are 
# the implicants of each compound.
#Purpose: Saves a Boolean logical model to an LP file.
def saveLPToFile(dict):
  logger = logging.getLogger("saveLP")
  logger.setLevel(logging.INFO)

  name = filename

  logger.debug("Filename: " + str(name))
  logger.debug("Path: " + str(write_folder))

  current_path = None
  current_path = os.path.join(write_folder, name.replace(".bnet", '.lp'))

  if not os.path.exists(os.path.dirname(current_path)):
    os.makedirs(os.path.dirname(current_path))
    logger.info("Created directory: " + str(current_path))

  f = open(current_path, 'w')
  result = ""
  logger.info("Saved to: " + str(current_path))
  
  all_compounds = getAllCompounds(dict, True)
  logger.debug("All compounds: " + str(all_compounds))

  if len(all_compounds) == len(list(dict.keys())):
    #If all compounds are present in the map keys, 
    # then the original order is preserved for convenience
    result = addCompoundsToResult(result, list(dict.keys())) 
  else: 
    result = addCompoundsToResult(result, all_compounds)  

  for function in dict.items():
    result = addRegulatorsToResult(result,function)
    result = addFunctionToResult(result,function)

  f.write(result)
  f.close()

#-----Main-----
if(cmd_enabled):
  parseArgs()

for fname in glob.glob(os.path.join(read_folder, filename)):
  with open(os.path.join(os.getcwd(), fname), 'r') as f:
    global_logger.debug("Reading file: " + filename)

    lines = [line.strip() for line in f.readlines()]
    func_dict = getFunctionDict(lines,global_logger)

    saveLPToFile(func_dict)

    