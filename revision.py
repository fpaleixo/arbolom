import os, argparse, logging, time, re
from genericpath import isdir
from aux_scripts.consistency_functions import *
from aux_scripts.conversion_functions import *
from aux_scripts.repair_constants import *
from aux_scripts.repair_functions import *
from aux_scripts.repair_prints import *

#Usage: $python revision.py -f (FILENAME) -o (OBSERVATIONS) -stable -sync -async -bulk -benchmark (SAVE_PATH)
#Optional flags:
#-stable -> Performs repairs using stable state observations (default).
#-sync -> Performs repairs using synchronous observations.
#-async -> Performs repairs using asynchronous observations.
#-bulk -> Enables bulk revision (-f must be path of the directory with the models)
#-benchmark -> Enables benchmark mode
#Variables:
#FILENAME -> Path of file containing the BCF Boolean model written in .lp or .bnet format
#OBSERVATIONS -> Path of file containing observations written in lp. 
#SAVE_PATH -> Path of folder to save benchmark results to


#-----Configs-----
#Toggle debug modes
iftv_debug_toggled = False

#Model path
model_path = None

#Paths of encodings with observations
obsv_path = None

#Flag that enables the revision of multiple models at once
bulk_enabled = False

#Flag that enables benchmark mode
# Note: Benchmark mode disables all prints, and produces an output file with
# four columns: the first is the name of the revised file, the second is
# whether it was inconsistent to begin with, 
# and if yes was it repaired successfully or not,
# the third is the time taken to revise it,
# and the fourth is only present in case of unsuccessful repairs, indicating
# which functions could not be repaired.
benchmark_enabled = False

benchmark_naming = False

#Benchmark save path
write_folder = "None"

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
global_logger.setLevel(logging.INFO)



#-----Auxiliary Functions-----
#---Argument parser---
#Purpose: Parses the arguments of function repair
def parseArgs():
  logger = logging.getLogger("parser")
  logger.setLevel(logging.INFO)

  global parser, args

  parser = argparse.ArgumentParser(description="Revise a Boolean logical model in the BCF written in .lp or .bnet format, given a set of observations written in .lp format.")
  requiredNamed = parser.add_argument_group("required arguments")
  requiredNamed.add_argument("-f", "--model_to_repair", help="Path of model to revise.", required=True)
  requiredNamed.add_argument("-o", "--observations", help="Path of observations from real-world model.", required=True)
  parser.add_argument("-stable", "--stable_state", action='store_true', help="Flag to check the consistency using stable state observations (default).")
  parser.add_argument("-sync", "--synchronous", action='store_true', help="Flag to check the consistency using synchronous observations (default is stable state).")
  parser.add_argument("-async", "--asynchronous", action='store_true', help="Flag to check the consistency using asynchronous observations (default is stable state).")
  parser.add_argument("-bulk", "--bulk", action='store_true', help="Enables the revision of multiple models at once. (Note: the path provided to -f must be the directory containing those models).")
  parser.add_argument("-benchmark", "--benchmark_save_folder", help="Enables benchmark mode, saving at the specified path.")
  parser.add_argument("-benchmark_naming", "--benchmark_naming", action='store_true', help="Enables benchmark files to be saved with a more helpful name.")
  args = parser.parse_args()

  global model_path, obsv_path, write_folder
  global toggle_stable_state, toggle_sync, toggle_async
  global bulk_enabled, benchmark_enabled, benchmark_naming

  model_path = args.model_to_repair
  obsv_path = args.observations

  logger.debug("Obtained model: " + model_path)
  logger.debug("Obtained observations: " + obsv_path)

  stable = args.stable_state
  synchronous = args.synchronous
  asynchronous = args.asynchronous
  bulk = args.bulk
  benchmark = args.benchmark_save_folder

  if bulk:
    bulk_enabled = bulk  
  
  if benchmark:
    benchmark_enabled = True
    if isdir(benchmark):
      write_folder = benchmark
    else:
      logger.info("Specified save location is not a valid directory. Saving in model directory instead.")
      write_folder = os.path.dirname(model_path)

  if args.benchmark_naming: 
    benchmark_naming = True

  if not stable and not synchronous and not asynchronous:
    logger.info("Default mode: Stable State \U0001f6d1")
    return

  if stable:
    toggle_stable_state = True
    toggle_sync = False
    toggle_async = False
    if not benchmark_naming: logger.info("Mode used: Stable State \U0001f6d1")

  elif synchronous:
    toggle_stable_state = False
    toggle_sync = True
    toggle_async = False
    if not benchmark_naming: logger.info("Mode used: Synchronous \U0001f550")

  elif asynchronous:
    toggle_stable_state = False
    toggle_sync = False
    toggle_async = True
    if not benchmark_naming: logger.info("Mode used: Asynchronous \U0001f331")
  return


#---Model reading-related functions---
def readModels():
  logger = logging.getLogger("readModels")
  logger.setLevel(logging.INFO)

  input_model_list = [model_path]
  output_model_list = []

  if bulk_enabled:
    input_model_list = [os.path.join(model_path, f) for f in os.listdir(model_path)
    if os.path.isfile(os.path.join(model_path,f)) and os.path.splitext(f)[1] == ".lp" or
    os.path.splitext(f)[1] == ".bnet"]
  
  for current_model_path in input_model_list:
    split_path = os.path.splitext(current_model_path)
    model_extension = split_path[1]

    if model_extension != ".bnet" and model_extension != ".lp":
      logger.error("Unrecognized model format. Only models written in "
      +".bnet or .lp format are accepted.")
      return None

    model_file = open(current_model_path, 'r')
    output_model = model_file.readlines()

    if model_extension == ".bnet":
      output_model = convertModelToLP(output_model,logger)
    
    else: output_model = "".join(output_model)
      
    logger.debug("obtained model: \n" + output_model)
    output_model_list.append((output_model,current_model_path))
  
  return output_model_list

def getModelCompounds(model):
  return re.findall('compound\((.+?)\).',model)


#-----Benchmarking Functions-----
def initRevisionStatsMap(model):
  revision_stats_map = {}
  all_compounds = sorted(getModelCompounds(model))

  for compound in all_compounds:
    revision_stats_map[compound] = {}
    revision_stats_map[compound][FINAL_STATE] = "consistent"
    revision_stats_map[compound][NODE_VARIATION] = 0
    revision_stats_map[compound][MISSING_REGULATORS] = 0
    revision_stats_map[compound][EXTRA_REGULATORS] = 0
    revision_stats_map[compound][CHANGED_SIGNS] = 0
    revision_stats_map[compound][MISSING_NODE_REGULATORS] = 0
    revision_stats_map[compound][EXTRA_NODE_REGULATORS] = 0

  return revision_stats_map

def fillBenchmarkArray(benchmark_array, model, final_state, 
  revision_time, consistency_time, repair_time, model_revision_stats):

  for func in model_revision_stats:
    benchmark_array.append(
      (model[1], 
      final_state, revision_time,
      consistency_time, repair_time,
      func, model_revision_stats[func][FINAL_STATE],
      model_revision_stats[func][NODE_VARIATION],
      model_revision_stats[func][MISSING_REGULATORS], model_revision_stats[func][EXTRA_REGULATORS],
      model_revision_stats[func][CHANGED_SIGNS],
      model_revision_stats[func][MISSING_NODE_REGULATORS],
      model_revision_stats[func][EXTRA_NODE_REGULATORS]
      )
    )

def processFunctionRepairStats(func, func_state, node_variation, functions, revision_stats):
  revision_stats[func][FINAL_STATE] = func_state
  revision_stats[func][NODE_VARIATION] = node_variation

  for atom in functions:
      if "missing_regulator" in atom:
        revision_stats[func][MISSING_REGULATORS] += 1 
      elif "extra_regulator" in atom:
        revision_stats[func][EXTRA_REGULATORS] += 1 
      elif "sign_changed" in atom:
        revision_stats[func][CHANGED_SIGNS] += 1 
      elif "missing_node_regulator" in atom: 
        revision_stats[func][MISSING_NODE_REGULATORS] += 1 
      elif "extra_node_regulator" in atom:
        revision_stats[func][EXTRA_NODE_REGULATORS] += 1 

def saveBenchmark(array):
  logger = logging.getLogger("saveBenchmark")
  logger.setLevel(logging.INFO)

  filename = None
  if benchmark_naming:
    filename = os.path.split(os.path.split(model_path)[0])[1] + "-" + os.path.basename(os.path.normpath(obsv_path))
  else:
    filename = os.path.basename(os.path.normpath(model_path)) + "-" + os.path.basename(os.path.normpath(obsv_path))


  if toggle_stable_state:
    filename += "-stable_benchmark.csv"
  elif toggle_sync:
    filename += "-sync_benchmark.csv"
  else:
    filename += "-async_benchmark.csv"
  
  save_path = None
  if write_folder:
    save_path = os.path.join(write_folder, filename)
  else:
    save_path = os.path.join(os.path.dirname(model_path), filename)
    if bulk_enabled:
      save_path = os.path.join(model_path, filename)

  logger.debug("Save path: " + str(save_path))

  f = open(save_path, 'w')

  for line in array:
    for column_idx in range(0,len(line)):
      f.write(str(line[column_idx]))

      if (column_idx != len(line)-1):
        f.write(",\t")
       
    f.write("\n")
  f.close()

  if not benchmark_naming: logger.info("Saved benchmark to: " + str(save_path))



#-----Revision Functions-----
def checkConsistency(model, obsv):
  logger = logging.getLogger("checkConsistency")
  logger.setLevel(logging.INFO)

  atoms = consistencyCheck(model,obsv,
    toggle_stable_state,toggle_sync,toggle_async)

  inconsistencies = isConsistent(atoms, toggle_stable_state, 
    toggle_sync, toggle_async, print_consistent=not benchmark_enabled)

  logger.debug("inconsistencies: \n" + str(inconsistencies))
  return inconsistencies 

def repair(model, inconsistencies, revision_stats): 
  incst_funcs = generateInconsistentFunctions(model, inconsistencies)
  i_f_array = processInconsistentFunctions(incst_funcs)
  final_state = "repaired"

  timed_out_functions = []
  unrepairable_functions = []

  if i_f_array:
    for func in i_f_array:
      func_state = "repaired"
      if not benchmark_enabled: printFuncRepairStart(func)

      prev_obs = generatePreviousObservations(func, inconsistencies, 
        toggle_sync, toggle_async)
      upo = processPreviousObservations(prev_obs)
      
      functions, node_variation = generateFunctions(func, model, inconsistencies, upo,
        toggle_stable_state, toggle_sync, toggle_async)

      if functions == "timed_out": 
        timed_out_functions.append(func)
        func_state = "inconsistent (timed out)"
        node_variation = 0

      elif functions == "no_solution": 
        unrepairable_functions.append(func)
        func_state = "inconsistent (no solution)"
        node_variation = 0

      processFunctionRepairStats(func, func_state, node_variation, functions, revision_stats)

      if not benchmark_enabled: printRepairedLP(func, functions, node_variation)
      if not benchmark_enabled: printFuncRepairEnd(func)
    
  if timed_out_functions and unrepairable_functions:
    final_state = "still inconsistent (timed out functions and functions without existing solutions)"
  elif timed_out_functions:
    final_state = "still inconsistent (timed out functions)"
  elif unrepairable_functions:
    final_state = "still inconsistent (functions without existing solutions)"

  return final_state



#-----Main-----
parseArgs()
# First, obtain the model in .lp model. If the obtained file has .bnet
# extension, it must be converted to .lp.
models = readModels()
benchmark_array = [(BCHMRK_MODEL_NAME, 
  BCHMRK_MODEL_STATE, BCHMRK_MODEL_REVISION_TIME,
  BCHMRK_MODEL_CONSISTENCY_TIME, BCHMRK_MODEL_REPAIR_TIME,
  BCHMRK_COMPOUND_NAME, BCHMRK_COMPOUND_STATE,
  BCHMRK_COMPOUND_NODE_VARIATION,
  BCHMRK_COMPOUND_MISSING_REGULATORS, BCHMRK_COMPOUND_EXTRA_REGULATORS,
  BCHMRK_COMPOUND_CHANGED_SIGNS,
  BCHMRK_COMPOUND_MISSING_NODE_REGULATORS,
  BCHMRK_COMPOUND_EXTRA_NODE_REGULATORS)]

for model in models:
  final_state = "consistent"
  revision_start_time = time.time()
  model_revision_stats = initRevisionStatsMap(model[0])

  if bulk_enabled and not benchmark_enabled: print("Currently revising model ", model[1])

  consistency_start_time = time.time()
  inconsistencies = checkConsistency(model[0], obsv_path)
  consistency_end_time = time.time()

  # Second, check the consistency of the .lp model using the provided observations
  # and time step. If the model is consistent, print a message saying so.
  if inconsistencies:
    if not benchmark_enabled: print("Inconsistent model! \nRepairing...")

    # Third, if it is not, proceed with the repairs and print out the necessary ones.
    repair_start_time = time.time()
    final_state = repair(model[0], inconsistencies, model_revision_stats)
    repair_end_time = time.time()
    
    if not benchmark_enabled and final_state == "repaired": print(f"Applying the above repairs to model {model[1]} will render it consistent!\n")

  revision_end_time = time.time()
  if benchmark_enabled:
    fillBenchmarkArray(benchmark_array, model, final_state,
      revision_end_time - revision_start_time, 
      consistency_end_time - consistency_start_time,
      repair_end_time - repair_start_time, model_revision_stats)

if benchmark_enabled:
  saveBenchmark(benchmark_array)


