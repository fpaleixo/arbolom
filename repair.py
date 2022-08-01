import argparse, logging, clingo, time
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
(no stable examples for boolean cell cycle)
python .\repair.py -f real_models/lp/corrupted/boolean_cell_cycle/boolean_cell_cycle-corrupted-f.lp -i real_models/lp/corrupted/boolean_cell_cycle/inconsistencies/boolean_cell_cycle-corrupted-f-sync_inconsistency.lp -sync
python .\repair.py -f real_models/lp/corrupted/boolean_cell_cycle/boolean_cell_cycle-corrupted-f.lp -i real_models/lp/corrupted/boolean_cell_cycle/inconsistencies/boolean_cell_cycle-corrupted-f-async_inconsistency.lp -async

#7 variables
python .\repair.py -i simple_models/lp/corrupted/11/inconsistencies/11-corrupted-f2-stable_inconsistency.lp -f simple_models/lp/corrupted/11/11-corrupted-f2.lp -stable
python .\repair.py -f simple_models/lp/corrupted/11/11-corrupted-f.lp -i simple_models/lp/corrupted/11/inconsistencies/11-corrupted-f-sync_inconsistency.lp -sync
python .\repair.py -f simple_models/lp/corrupted/11/11-corrupted-f.lp -i simple_models/lp/corrupted/11/inconsistencies/11-corrupted-f-async_inconsistency.lp -async

#8 variables
(no stable examples for sp1 cell)
python .\repair.py -f real_models/lp/corrupted/SP_1cell/SP_1cell-corrupted-f.lp -i real_models/lp/corrupted/SP_1cell/inconsistencies/SP_1cell-corrupted-f-sync_inconsistency.lp -sync
(no async examples)

#All functions inconsistent
python .\repair.py -f simple_models/lp/corrupted/6/6-corrupted-fe.lp -i simple_models/lp/corrupted/6/inconsistencies/6-corrupted-fe-stable_inconsistency.lp -stable
python .\repair.py -f simple_models/lp/corrupted/6/6-corrupted-fe.lp -i simple_models/lp/corrupted/6/inconsistencies/6-corrupted-fe-sync_inconsistency.lp -sync
python .\repair.py -f simple_models/lp/corrupted/6/6-corrupted-fe.lp -i simple_models/lp/corrupted/6/inconsistencies/6-corrupted-fe-async_inconsistency.lp -async

#Total of 30 variables, with functions of varying variable number
.\repair.py -f simple_models/lp/corrupted/13/13-corrupted-fera.lp -i simple_models/lp/corrupted/13/inconsistencies/13-corrupted-fera-sync_inconsistency.lp -sync

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

#Path of the encodings to obtain inconsistent functions and total variables of each of those functions
iftv_path = "encodings/repairs/auxiliary/iftv.lp"

#Paths of the encoding to identify unique positive observations
unique_positive_observations_path = "encodings/repairs/auxiliary/upo.lp"
unique_positive_observations_async_path = "encodings/repairs/auxiliary/upo_async.lp"

#Variables of python implementation of unique positive observations
previous_observations_sync_path = "encodings/repairs/auxiliary/previous_observations_sync.lp"
previous_observations_async_path = "encodings/repairs/auxiliary/previous_observations_async.lp"
processed_upo = ""

#Paths of encodings for generating functions
repair_encoding_stable_path = "encodings/repairs/repairs_stable.lp"
repair_encoding_sync_path = "encodings/repairs/repairs_sync.lp"
repair_encoding_async_path = "encodings/repairs/repairs_async.lp"

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

#---Printing functions---
#Input: stats_dict dictionary from clingo.Control
#Purpose: Prints time statistics from clingo
def printStatistics(stats_dict):
  times = stats_dict["summary"]["times"]
  print("\n<Statistics>")
  print("Total: "+str(times["total"]) + "s (Solving: "+str(times["solve"])+"s)")
  print("CPU Time: "+str(times["cpu"])+"s")
  print("\n")



#-----Functions that create the LPs to be used by clingo-----
#Purpose: Separates the inconsistencies from the curated observations that are outputted as an LP from the consistency checking phase
def getInconsistenciesAndCuratedLP():
  inconsistencies = open(incst_path, 'r')
  lines = inconsistencies.readlines()

  incst_LP = ""
  curated_LP = ""

  for line in lines: 
    if "inconsistent" in line:
      incst_LP += line
    else:
      curated_LP += line

  return incst_LP, curated_LP

#Input: The nodes generated from clingo
#Purpose: Creates a map of logic programs, indexed by inconsistent functions. Each value contains a string with the variables and total number of variables
# of the respective inconsistent function.
def getIftvsLPAndTotalVars(iftvs):
  result_LP = {}
  total_vars = {}

  for iftv in iftvs:
    current_LP = ""
    var_name = ""
      
    var_name = iftv[0].split(')')[0].split('(')[1]
    
    for atom_idx in range(1, len(iftv)):
      current_LP += iftv[atom_idx] +".\n"

    result_LP[var_name] = current_LP
    total_vars[var_name] = int(iftv[-1].split(')')[0].split('(')[1])

  return result_LP, total_vars



#-----Functions that process output from clingo-----
#Input: The generated iftv output from clingo
#Purpose: Processes clingo's iftv output by creating an LP with them, forming a map with inconsistent functions as keys and the respective
# LP containing the variables and total number of variables as value 
def processIFTVs(iftvs):
  if not iftvs:
    print("No answers sets could be found	\u2755 there must be something wrong with the encoding...")

  elif iftvs[0]:

    iftvs_LP, total_vars = getIftvsLPAndTotalVars(iftvs)

    total_iftvs = len(iftvs)
    if(total_iftvs < 100):
      print("<Resulting inconsistent functions and total variables>")
      print(str(iftvs_LP),end="\n\n")
    else:
      print("Too many iftvs to print...!")
    print(f"Total iftvs: {total_iftvs}\n")

    return iftvs_LP, total_vars

  else: 
    print("No iftvs could be found \u274C")



#-----Functions that solve LPs with clingo-----
#Input: The LP containing information regarding the inconsistent functions
#Purpose: Obtains inconsistent functions, the variables and total number of variables of each function
def generateInconsistentFunctionsAndTotalVars(incst_LP):
  clingo_args = ["0"]
  if iftv_debug_toggled:
    clingo_args.append("--output-debug=text")

  ctl = clingo.Control(arguments=clingo_args, logger= lambda a,b: None)

  ctl.add("base",[], program=incst_LP)
  ctl.load(model_path)
  ctl.load(iftv_path)

  print("Starting iftv generation \u23F1")
  ctl.ground([("base", [])])
  iftv = []

  with ctl.solve(yield_=True) as handle:
    for model in handle:
      iftv.append(str(model).split(" "))

  print("Finished iftv generation \U0001F3C1")
  printStatistics(ctl.statistics)
  return iftv

#Inputs: The inconsistent compound's function, and the LP containing the curated observations
#Purpose: Generates a function compatible with the given set of curated observations
def generateFunctions(func):
  print("Calculating optimal repairs...")
  clingo_args = ["0", f"-c compound={func}"]
    
  ctl = clingo.Control(arguments=clingo_args, logger= lambda a,b: None)

  ctl.add("base", [], program=processed_upo)
  ctl.load(incst_path)
  ctl.load(model_path) 

  if toggle_stable_state:
    ctl.load(repair_encoding_stable_path)
  elif toggle_sync:
    ctl.load(repair_encoding_sync_path)
  else:
    ctl.load(repair_encoding_async_path)
  
  ctl.ground([("base", [])])
  functions = []

  with ctl.solve(yield_=True) as handle:
    for model in handle:
      functions = str(model).split(" ")
  
  print("... Done.")
  printStatistics(ctl.statistics)
  return functions



#-----Python implementation of unique positive observation determination-----
#Inputs: 
# -func, the compound that has the inconsistent function, 
# -curated_LP, the LP containing all curated observations
#Purpose: Returns observations that happen in the timestep before
# positive observations
def generatePreviousObservations(func, curated_LP):
  print("Calculating previous observations...")
  clingo_args = ["0", f"-c compound={func}"]
  
  ctl = clingo.Control(arguments=clingo_args)

  ctl.add("base", [], program=curated_LP)

  if toggle_sync:
    ctl.load(previous_observations_sync_path)
  elif toggle_async:
    ctl.load(previous_observations_async_path)
  else: 
    return []
  
  ctl.ground([("base", [])])
  functions = []

  with ctl.solve(yield_=True) as handle:
    for model in handle:
      functions = str(model).split(" ")

  print("... Done.")

  printStatistics(ctl.statistics)

  if not functions[0]: #If there are no previous observations
    return []

  return functions

#Inputs: 
# -prev_obs, a string containing all previous observations
#Purpose: Returns all unique positive observations
def processPreviousObservations(prev_obs):

  if not prev_obs:
    return ""
    
  uniques_map = {}

  output = ""

  current_experiment = ""
  current_timestep = ""
  current_state_key = "0"

  start = time.time()
  for previous_obsv in prev_obs:
    arguments = previous_obsv.split(')')[0].split('(')[1].split(',')
    experiment = arguments[0]
    timestep = arguments[1]
    compound = arguments[2]
    state = arguments[3]

    #First iteration
    if not current_experiment:
      current_experiment = experiment
      current_timestep = timestep

    #If we're still looking at the same experiment and timestep
    if current_experiment + current_timestep == experiment + timestep:

      #If the compound is active, it will be a part of this timestep's 
      # state key
      if state == "1":
        current_state_key += compound

    else: #We are looking at a different experiment or timestep

      #Save previous timestep's state in the map, if it didn't exist yet
      sorted_state = "".join(sorted(current_state_key))

      if sorted_state not in uniques_map:
          uniques_map[sorted_state] = current_experiment + ","+ str(int(current_timestep) + 1)
   
      current_experiment = experiment
      current_timestep = timestep
      current_state_key = "0"

      if state == "1":
        current_state_key += compound

  #End of loop, last timestep's state must be saved
  sorted_state = "".join(sorted(current_state_key))

  if sorted_state not in uniques_map:
    uniques_map[sorted_state] = current_experiment + ","+ str(int(current_timestep) + 1)

  #Print result in LP format
  for value in uniques_map.values():
    output += "unique_positive_observation(" + value + ").\n"

  end = time.time()
  print(f"Python code time for unique positive observations: {end - start}s\n")
  return output



#-----Main-----
if cmd_enabled:
  parseArgs()

  start_time = time.time()
  printIFTVStart()
  incst_LP, curated_LP = getInconsistenciesAndCuratedLP()

  iftvs = generateInconsistentFunctionsAndTotalVars(incst_LP)
  iftvs_LP, total_vars = processIFTVs(iftvs)
  printIFTVEnd()

  if iftvs_LP:
    for func in iftvs_LP.keys():

      printFuncRepairStart(func)
      
      prev_obs = generatePreviousObservations(func, curated_LP)
      uniques = processPreviousObservations(prev_obs)
      processed_upo = uniques
      
      functions = generateFunctions(func)
      printRepairedLP(func, functions)
      
      printFuncRepairEnd(func)

  end_time = time.time()
  print(f"Total time taken: {end_time-start_time}s", )
  