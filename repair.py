import argparse, logging, time
from aux_scripts.repair_functions import *
from aux_scripts.repair_prints import *

#Usage: $python repair.py -f (FILENAME) -i (INCONSISTENCIES) -stable -sync -async
#Optional flags:
#-stable -> Performs repairs using stable state observations (default).
#-sync -> Performs repairs using synchronous observations.
#-async -> Performs repairs using asynchronous observations.
#Variables:
#FILENAME -> Path of file containing Boolean model in the BCF format written in lp.
#INCONSISTENCIES -> Path of file containing inconsistencies obtained from the consistency checking phase.


#-----Testing shortcuts (to be removed at a later date)----
'''
#3 variables
python .\repair.py -f simple_models/lp/corrupted/3/3-corrupted-f.lp -i simple_models/lp/corrupted/3/inconsistencies/3-corrupted-f-stable_inconsistency.lp -stable
python .\repair.py -f simple_models/lp/corrupted/3/3-corrupted-f.lp -i simple_models/lp/corrupted/3/inconsistencies/3-corrupted-f-sync_inconsistency.lp -sync
python .\repair.py -f simple_models/lp/corrupted/3/3-corrupted-f.lp -i simple_models/lp/corrupted/3/inconsistencies/3-corrupted-f-async_inconsistency.lp -async

#5 variables
python .\repair.py -f simple_models/lp/corrupted/8/8-corrupted-f.lp -i simple_models/lp/corrupted/8/inconsistencies/8-corrupted-f-stable_inconsistency.lp -stable
python .\repair.py -f simple_models/lp/corrupted/8/8-corrupted-f.lp -i simple_models/lp/corrupted/8/inconsistencies/8-corrupted-f-sync_inconsistency.lp -sync
python .\repair.py -f simple_models/lp/corrupted/8/8-corrupted-f.lp -i simple_models/lp/corrupted/8/inconsistencies/8-corrupted-f-async_inconsistency.lp -async

#6 variables
python .\repair.py -f real_models/lp/corrupted/boolean_cell_cycle/boolean_cell_cycle-corrupted-f.lp -i real_models/lp/corrupted/boolean_cell_cycle/inconsistencies/boolean_cell_cycle-corrupted-f-stable_inconsistency.lp
python .\repair.py -f real_models/lp/corrupted/boolean_cell_cycle/boolean_cell_cycle-corrupted-f.lp -i real_models/lp/corrupted/boolean_cell_cycle/inconsistencies/boolean_cell_cycle-corrupted-f-sync_inconsistency.lp -sync
python .\repair.py -f real_models/lp/corrupted/boolean_cell_cycle/boolean_cell_cycle-corrupted-f.lp -i real_models/lp/corrupted/boolean_cell_cycle/inconsistencies/boolean_cell_cycle-corrupted-f-async_inconsistency.lp -async

#7 variables
python .\repair.py -i simple_models/lp/corrupted/11/inconsistencies/11-corrupted-f2-stable_inconsistency.lp -f simple_models/lp/corrupted/11/11-corrupted-f2.lp -stable
python .\repair.py -f simple_models/lp/corrupted/11/11-corrupted-f.lp -i simple_models/lp/corrupted/11/inconsistencies/11-corrupted-f-sync_inconsistency.lp -sync
python .\repair.py -f simple_models/lp/corrupted/11/11-corrupted-f.lp -i simple_models/lp/corrupted/11/inconsistencies/11-corrupted-f-async_inconsistency.lp -async

#8 variables
python .\repair.py -f real_models/lp/corrupted/SP_1cell/SP_1cell-corrupted-f.lp -i real_models/lp/corrupted/SP_1cell/inconsistencies/SP_1cell-corrupted-f-stable_inconsistency.lp
python .\repair.py -f real_models/lp/corrupted/SP_1cell/SP_1cell-corrupted-f.lp -i real_models/lp/corrupted/SP_1cell/inconsistencies/SP_1cell-corrupted-f-sync_inconsistency.lp -sync
python .\repair.py -f real_models/lp/corrupted/SP_1cell/SP_1cell-corrupted-f.lp -i real_models/lp/corrupted/SP_1cell/inconsistencies/SP_1cell-corrupted-f-async_inconsistency.lp -async

#All functions inconsistent
python .\repair.py -f simple_models/lp/corrupted/6/6-corrupted-fe.lp -i simple_models/lp/corrupted/6/inconsistencies/6-corrupted-fe-stable_inconsistency.lp -stable
python .\repair.py -f simple_models/lp/corrupted/6/6-corrupted-fe.lp -i simple_models/lp/corrupted/6/inconsistencies/6-corrupted-fe-sync_inconsistency.lp -sync
python .\repair.py -f simple_models/lp/corrupted/6/6-corrupted-fe.lp -i simple_models/lp/corrupted/6/inconsistencies/6-corrupted-fe-async_inconsistency.lp -async

#Total of 30 variables, with functions of varying variable number
.\repair.py -f simple_models/lp/corrupted/13/13-corrupted-fera.lp -i simple_models/lp/corrupted/13/inconsistencies/13-corrupted-fera-sync_inconsistency.lp -sync

#Real world model with 40 variables
.\repair.py -f real_models/lp/corrupted/TCRsig40/TCRsig40-corrupted-fera.lp -i real_models/lp/corrupted/TCRsig40/inconsistencies/TCRsig40-corrupted-fera-sync_inconsistency.lp -sync

#NO SOLUTIONS
#6 variables
python .\repair.py -f real_models/lp/corrupted/boolean_cell_cycle/boolean_cell_cycle-corrupted-f.lp -i testing/impossible_inconsistencies/boolean_cell_cycle-corrupted-f-sync_inconsistency.lp -sync 

#8 variables
python .\repair.py -f real_models/lp/corrupted/SP_1cell/SP_1cell-corrupted-f.lp -i testing/impossible_inconsistencies/SP_1cell-corrupted-f-sync_inconsistency.lp -sync
'''


#-----Configs-----
#Command-line usage
cmd_enabled = True

#Toggle debug modes
iftv_debug_toggled = False

#Model path
model_path = "simple_models/lp/corrupted/8/8-corrupted-f.lp"

#Paths of encodings with inconsistencies
incst_path = "simple_models/lp/corrupted/8/inconsistencies/8-corrupted-f-sync_inconsistency.lp"

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

  parser = argparse.ArgumentParser(description="Repair an inconsistent Boolean logical model in the BCF written in lp, given a set of observations and inconsistent compounds, both written in lp.")
  parser.add_argument("-f", "--model_to_repair", help="Path to model to check the consistency of.", required=True)
  parser.add_argument("-i", "--inconsistencies", help="Path to inconsistencies obtained from the consistency checking phase.", required=True)
  parser.add_argument("-stable", "--stable_state", action='store_true', help="Flag to check the consistency using stable state observations (default).")
  parser.add_argument("-sync", "--synchronous", action='store_true', help="Flag to check the consistency using synchronous observations (default is stable state).")
  parser.add_argument("-async", "--asynchronous", action='store_true', help="Flag to check the consistency using asynchronous observations (default is stable state).")
  args = parser.parse_args()

  global model_path, incst_path, toggle_stable_state, toggle_sync, toggle_async

  model_path = args.model_to_repair
  incst_path = args.inconsistencies

  logger.debug("Obtained model: " + model_path)
  logger.debug("Obtained inconsistencies: " + incst_path)


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
if cmd_enabled:
  parseArgs()

  start_time = time.time()
  printIFTVStart()

  incst_funcs = generateInconsistentFunctions(model_path, incst_path, 
    iftv_debug_toggled, True, True)
  i_f_array = processInconsistentFunctions(incst_funcs, True)
  printIFTVEnd()

  if i_f_array:
    for func in i_f_array:

      printFuncRepairStart(func)
      
      prev_obs = generatePreviousObservations(func, incst_path, toggle_sync,
        toggle_async, True, True)
      upo = processPreviousObservations(prev_obs)
      
      functions = generateFunctions(func, model_path, incst_path, upo,
        toggle_stable_state, toggle_sync, toggle_async, True, True)

      printRepairedLP(func, functions)
      
      printFuncRepairEnd(func)

  end_time = time.time()
  print(f"Total time taken: {end_time-start_time}s", )
  