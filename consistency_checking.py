import os, argparse, logging, glob, clingo, re
from clingo.application import ApplicationOptions
from common import uniquify

#TODO - stable state encoding

#-----Configs-----

#Command-line usage
cmd_enabled = False

#Model path
model_path = "./lp_models/1.lp"

#Observations path
obsv_path = "./lp_models/obsv/sstate/1-obs.lp" 

#Mode flags 
toggle_stable_state = True
toggle_sync = False
toggle_async = False

#Encoding paths
ss_path = "./encodings/ss_consistency.lp"
sync_path = "./encodings/sync_consistency.lp"
async_path = "./encodings/async_consistency.lp"

#Parser (will only be used if command-line usage is enabled above)
parser = None
args = None
if(cmd_enabled):
  parser = argparse.ArgumentParser(description="Check the consistency of a Boolean logical model in the BCF written in lp, given a set of observations in lp.")
  parser.add_argument("-f", "--model_to_check", help="Path to model to check the consistency of.")
  parser.add_argument("-o", "--observations_to_use", help="Path to observations used to check the consistency of the model.")
  parser.add_argument("-stable", "--stable_state", action='store_true', help="Flag to check the consistency using stable state observations (default).")
  parser.add_argument("-sync", "--synchronous", action='store_true', help="Flag to check the consistency using synchronous observations (default is stable state).")
  parser.add_argument("-async", "--asynchronous", action='store_true', help="Flag to check the consistency using asynchronous observations (default is stable state).")
  args = parser.parse_args()

#Global logger (change logging.(LEVEL) to desired (LEVEL) )
logging.basicConfig()
global_logger = logging.getLogger("global")
global_logger.setLevel(logging.DEBUG)



#-----Auxiliary Functions-----

#Purpose: Parses the argument regarding which file to generate observations for.
def parseArgs():
  logger = logging.getLogger("parser")
  logger.setLevel(logging.DEBUG)

  global model_path, obsv_path, toggle_stable_state, toggle_sync, toggle_async

  model_path = args.model_to_check

  logger.debug("Obtained file: " + model_path)

  obsv = args.observations_to_use
  stable = args.stable_state
  synchronous = args.synchronous
  asynchronous = args.asynchronous

  if obsv:
    obsv_path = obsv

  if stable:
    toggle_stable_state = True
    toggle_sync = False
    toggle_async = False
    logger.debug("Mode used: stable state.")

  elif synchronous:
    toggle_stable_state = False
    toggle_sync = True
    toggle_async = False
    logger.debug("Mode used: synchronous.")

  elif asynchronous:
    toggle_stable_state = False
    toggle_sync = False
    toggle_async = True
    logger.debug("Mode used: asynchronous.")

  return


#Input: Model outputted from clingo
#Purpose: Prints the obtained model after solving
def on_model(m):
  print (m)


def isConsistent(atoms):
  print("TODO")



#-----Main-----
if(cmd_enabled):
  parseArgs()

ctl = clingo.Control()

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
    print(model)
    atoms += (str(model).split(" "))

isConsistent(atoms)
