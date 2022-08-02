import argparse, logging, clingo, time
import os
from aux_scripts.common import getAllCompounds
from aux_scripts.consistency_functions import *
from aux_scripts.conversion_functions import *
from aux_scripts.repair_prints import *

#Usage: $python revision.py -f (FILENAME) -o (OBSERVATIONS) -stable -sync -async
#Optional flags:
#-stable -> Performs repairs using stable state observations (default).
#-sync -> Performs repairs using synchronous observations.
#-async -> Performs repairs using asynchronous observations.
#Variables:
#FILENAME -> Path of file containing the BCF Boolean model written in .lp or .bnet format
#OBSERVATIONS -> Path of file containing observations written in lp. 


#-----Configs-----
#Toggle debug modes
iftv_debug_toggled = False

#Model path
model_path = None

#Paths of encodings with inconsistencies
obsv_path = None

#Mode flags 
toggle_stable_state = True
toggle_sync = False
toggle_async = False

#Parser (will only be used if command-line usage is enabled above)
parser = None
args = None

#Global logger (change logging.(LEVEL) to desired (LEVEL) )
logging.basicConfig()
global_logger = logging.getLogger("global")
global_logger.setLevel(logging.DEBUG)



#-----Auxiliary Functions-----
#---Argument parser---
#Purpose: Parses the arguments of function repair
def parseArgs():
  logger = logging.getLogger("parser")
  logger.setLevel(logging.INFO)

  global parser, args

  parser = argparse.ArgumentParser(description="Revise a Boolean logical model in the BCF written in .lp or .bnet format, given a set of observations written in .lp format.")
  parser.add_argument("-f", "--model_to_repair", help="Path of model to revise.", required=True)
  parser.add_argument("-o", "--observations", help="Path of observations from real-world model.", required=True)
  parser.add_argument("-stable", "--stable_state", action='store_true', help="Flag to check the consistency using stable state observations (default).")
  parser.add_argument("-sync", "--synchronous", action='store_true', help="Flag to check the consistency using synchronous observations (default is stable state).")
  parser.add_argument("-async", "--asynchronous", action='store_true', help="Flag to check the consistency using asynchronous observations (default is stable state).")
  args = parser.parse_args()

  global model_path, obsv_path, toggle_stable_state, toggle_sync, toggle_async

  model_path = args.model_to_repair
  obsv_path = args.observations

  logger.debug("Obtained model: " + model_path)
  logger.debug("Obtained observations: " + obsv_path)

  stable = args.stable_state
  synchronous = args.synchronous
  asynchronous = args.asynchronous

  if not stable and not synchronous and not asynchronous:
    logger.info("Default mode: Stable State \U0001f6d1")
    return

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


#-----Convertion Functions-----
def convertModelToLP(model):
  logger = logging.getLogger("saveLP")
  logger.setLevel(logging.INFO)

  lines = [line.strip() for line in model]
  func_dict = getFunctionDict(lines, logger)

  result = ""
  
  all_compounds = getAllCompounds(func_dict, True)
  logger.debug("All compounds: " + str(all_compounds))

  if len(all_compounds) == len(list(func_dict.keys())):
    #If all compounds are present in the map keys, 
    # then the original order is preserved for convenience
    result = addCompoundsToResult(result, list(func_dict.keys())) 
  else: 
    result = addCompoundsToResult(result, all_compounds)  

  for function in func_dict.items():
    result = addRegulatorsToResult(result,function)
    result = addFunctionToResult(result,function)

  return result


#-----Revision Functions-----
def readModel():
  logger = logging.getLogger("readModel")
  logger.setLevel(logging.INFO)

  split_path = os.path.splitext(model_path)
  model_extension = split_path[1]

  if model_extension != ".bnet" and model_extension != ".lp":
    logger.error("Unrecognized model format. Only models written in "
    +".bnet or .lp format are accepted.")
    return None

  model_file = open(model_path, 'r')
  model = model_file.readlines()

  if model_extension == ".bnet":
    print("conversion happens here")
    model = convertModelToLP(model)
  
  else: model = "".join(model)
    
  logger.debug("obtained model: \n" + model)
  return model


def checkConsistency(model, obsv):
  logger = logging.getLogger("checkConsistency")
  logger.setLevel(logging.INFO)

  atoms = consistencyCheck(model,obsv,
    toggle_stable_state,toggle_sync,toggle_async)
  inconsistencies = isConsistent(atoms, toggle_stable_state, 
    toggle_sync, toggle_async)

  logger.debug("inconsistencies: \n" + str(inconsistencies))
  return inconsistencies


def repair(model, inconsistencies):
  repairs = ""
  print("repairs happen here")

  return repairs


#-----Main-----
parseArgs()
# First, obtain the model in .lp model. If the obtained file has .bnet
# extension, it must be converted to .lp.
model = readModel()
if model:
  inconsistencies = checkConsistency(model, obsv_path)

  # Second, check the consistency of the .lp model using the provided observations
  # and time step.
  if not inconsistencies:
    print("The model is consistent with the observations \u2714\uFE0F")
  else: 
    print("Inconsistent model. Repairing...")
    repairs = repair(model, inconsistencies)

    # Third, if the model is consistent, print a message saying so. If it is not,
    #proceed with the repairs and print out the necessary ones.
    if not repairs:
      print("No repairs could be found \u274C")
    else:
      print("Repairs found \u2714\uFE0F")
      print("Print repairs here")


