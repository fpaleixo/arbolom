import os, argparse, logging, clingo

#Usage: $python consistency_checking.py -f (FILENAME) -o (OBSERVATIONS) -stable -sync -async -s (SAVE_DIRECTORY)

#Optional flags:
#-stable -> Performs consistency checking using stable state observations (default).
#-sync -> Performs consistency checking using synchronous observations.
#-async -> Performs consistency checking using asynchronous observations.
#-s -> Path of directory to save inconsistencies, when they exist (default is lp_models/corrupted/(name_of_file))

#Variables:
#FILENAME -> Path of file containing Boolean model in the BCF format written in lp.
#OBSERVATIONS -> Path of file containing observations written in lp. 

#Attention: 
# File FILENAME must be in the BCF format and follow the conventions of the 
# .lp files in the lp_models folder (results will be unpredictable otherwise).
#Observations should also follow the conventions of the files in the 
# obsv folder, inside lp_models.


#-----Configs-----
#Command-line usage
cmd_enabled = True

#Model path
model_path = "simple_models/lp/corrupted/1/1-corrupted-era.lp"

#Observations path
obsv_path = "simple_models/lp/observations/sstate/1-obs.lp" 

#Inconsistencies save path
write_folder = "simple_models/lp/corrupted" 

#Mode flags 
toggle_stable_state = True
toggle_sync = False
toggle_async = False

#Encoding paths
ss_path = "./encodings/consistency/ss_consistency.lp"
sync_path = "./encodings/consistency/sync_consistency.lp"
async_path = "./encodings/consistency/async_consistency.lp"

#Parser (will only be used if command-line usage is enabled above)
parser = None
args = None
if(cmd_enabled):
  parser = argparse.ArgumentParser(description=
    "Check the consistency of a Boolean logical model in the BCF written in " + 
    " lp, given a set of observations in lp.")
  parser.add_argument("-f", "--model_to_check", help=
    "Path to model to check the consistency of.")
  parser.add_argument("-o", "--observations_to_use", help=
    "Path to observations used to check the consistency of the model.")
  parser.add_argument("-stable", "--stable_state", action='store_true', help=
    "Flag to check the consistency using stable state observations (default).")
  parser.add_argument("-sync", "--synchronous", action='store_true', help=
    "Flag to check the consistency using synchronous observations (default is stable state).")
  parser.add_argument("-async", "--asynchronous", action='store_true', help=
    "Flag to check the consistency using asynchronous observations (default is stable state).")
  parser.add_argument("-s", "--save_directory", help=
    "Path of directory to save inconsistent functions to (if they exist).")
  args = parser.parse_args()

#Global logger (change logging.(LEVEL) to desired (LEVEL) )
logging.basicConfig()
global_logger = logging.getLogger("global")
global_logger.setLevel(logging.INFO)



#-----Auxiliary Functions-----
#Purpose: Parses the argument regarding which file to generate observations for.
def parseArgs():
  logger = logging.getLogger("parser")
  logger.setLevel(logging.DEBUG)

  global model_path, write_folder, obsv_path
  global toggle_stable_state, toggle_sync, toggle_async

  model_path = args.model_to_check
  write_folder = os.path.dirname(model_path)
  write_folder = os.path.join(write_folder, "inconsistencies")

  logger.debug("Obtained model: " + model_path)

  obsv = args.observations_to_use
  stable = args.stable_state
  synchronous = args.synchronous
  asynchronous = args.asynchronous

  if(args.save_directory):
    write_folder = args.save_directory
    logger.debug("Write folder is: "+ write_folder)

  if obsv:
    obsv_path = obsv
    logger.debug("Obtained observations: " + obsv_path)

  if stable:
    toggle_stable_state = True
    toggle_sync = False
    toggle_async = False
    logger.info("Mode used: Stable State \U0001f6d1")

  elif synchronous:
    toggle_stable_state = False
    toggle_sync = True
    toggle_async = False
    logger.info("Mode used: Synchronous \U0001f550")

  elif asynchronous:
    toggle_stable_state = False
    toggle_sync = False
    toggle_async = True
    logger.info("Mode used: Asynchronous \U0001f331")

  return

#Inputs: atoms is a list of atoms obtained from solving with clingo.
#Purpose: Stores inconsistency atoms in a separate file 
# (to be used by repairs later on).
def saveInconsistenciesToFile(LP):
  logger = logging.getLogger("saveIncst")
  logger.setLevel(logging.INFO)

  global write_folder

  filename = os.path.basename(model_path)

  if toggle_stable_state:
    filename = filename.replace(".lp", "-stable_inconsistency.lp")
  elif toggle_sync:
    filename = filename.replace(".lp", "-sync_inconsistency.lp")
  else:
    filename = filename.replace(".lp", "-async_inconsistency.lp")

  logger.debug("Filename: " + str(filename))

  if not os.path.exists(write_folder):
    os.makedirs(write_folder)
    logger.info("Created directory: " + str(write_folder))

  write_fullpath = os.path.join(write_folder, filename)

  logger.debug("Full path: " + str(write_fullpath))

  f = open(write_fullpath, 'w')
  f.write(LP)
  f.close()

  logger.info("Saved to: " + str(write_fullpath))

#Inputs: atoms is a list of atoms obtained from solving with clingo.
#Purpose: Prints the obtained atoms in a more readable manner.
def isConsistent(atoms):
  if not atoms:
    print("No answers sets could be found	\u2755 there must be something wrong with the encoding...")
  else:
    isConsistent = True
    inconsistent_LP = ""
    observations_LP = ""

    for atom in atoms:
      if "inconsistent" in atom:
        isConsistent = False
        inconsistent_LP += atom + ".\n"
      else:
        observations_LP += atom + ".\n"

    if not isConsistent:
      if toggle_stable_state:
        print("Model is not consistent \u274C Inconsistent (experiment, compound, value): ")
      elif toggle_sync:
        print("Model is not consistent \u274C Inconsistent (experiment, timestep, compound, value): ")
      else:
        print("Model is not consistent \u274C Inconsistent (experiment, timestep, compound, value/other compound updated at the same time): ")  
      print(inconsistent_LP)
      saveInconsistenciesToFile(inconsistent_LP + "\n" + observations_LP)
    
    else: 
      print("Model is consistent \u2714\uFE0F")


#-----Main-----
if(cmd_enabled):
  parseArgs()

ctl = clingo.Control(arguments=["0"])

ctl.load(model_path)
ctl.load(obsv_path)

if toggle_stable_state:
  ctl.load(ss_path)
elif toggle_sync:
  ctl.load(sync_path)
else:
  ctl.load(async_path)

ctl.ground([("base", [])])
atoms = []
with ctl.solve(yield_=True) as handle:
  for model in handle:
    atoms = (str(model).split(" "))

isConsistent(atoms)