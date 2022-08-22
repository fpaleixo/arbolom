import os, argparse, logging, time
from aux_scripts.consistency_functions import *
from aux_scripts.conversion_functions import *
from aux_scripts.repair_functions import *
from aux_scripts.repair_prints import *

#Usage: $python benchmark.py -f (CONFIG_FOLDER) -o (OBSERVATION_FOLDER) -m (MODEL_NAME) -s (SAVE_FOLDER) -stable -sync -async
#Optional flags:
#-stable -> Performs repairs using stable state observations (default).
#-sync -> Performs repairs using synchronous observations.
#-async -> Performs repairs using asynchronous observations.
#Variables:
#CONFIG_FOLDER -> Path of file containing the BCF Boolean model written in .lp or .bnet format.
#OBSERVATION_FOLDER -> Path of file containing observations written in lp. 
#MODEL_NAME -> The name of the model that will be benchmarked.
#INTERACTION_TYPE -> The interaction type to be considered (stable, sync or async).
#SAVE_FOLDER -> The folder where the results from benchmarking will be saved to.

#-----Configs-----
#Config folder path
config_path = None

#Paths of folder with observations
obsv_path = None

#Model name
model_name = None

#Paths of encodings with inconsistencies
obsv_path = None

#Folder where the benchmark results will be saved to
save_folder = None

#Mode flags 
toggle_stable_state = True
toggle_sync = False
toggle_async = False

#Parser
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

  parser = argparse.ArgumentParser(description="Benchmark the ARBoLoM tool using the benchmarking folder structure presented in the project's page.")
  requiredNamed = parser.add_argument_group("required arguments")
  requiredNamed.add_argument("-f", "--config_folder", help="Path of folder containing config folders.", required=True)
  requiredNamed.add_argument("-o", "--observations", help="Path of observations from real-world models.", required=True)
  requiredNamed.add_argument("-m", "--model_name", help="Name of the model to benchmark (doesn't need to be exact, just needs to be contained in it).", required=True)
  requiredNamed.add_argument("-s", "--save_folder", help="Path of folder to save benchmarks to.", required=True)
  parser.add_argument("-stable", "--stable_state", action='store_true', help="Flag to benchmark using stable state observations (default).")
  parser.add_argument("-sync", "--synchronous", action='store_true', help="Flag to benchmark using synchronous observations (default is stable state).")
  parser.add_argument("-async", "--asynchronous", action='store_true', help="Flag to benchmark using asynchronous observations (default is stable state).")
  args = parser.parse_args()

  global config_path, obsv_path, model_name, save_folder
  global toggle_stable_state, toggle_sync, toggle_async

  config_path = args.config_folder
  obsv_path = args.observations
  save_folder = args.save_folder

  logger.debug("Obtained configs folder: " + config_path)
  logger.debug("Obtained observations folder: " + obsv_path)
  logger.debug("Obtained save folder: " + save_folder)


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


#-----Main-----
parseArgs()


