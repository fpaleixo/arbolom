import os, argparse, logging, time
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



#-----Revision Functions-----
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


def checkConsistency(model, obsv):
  logger = logging.getLogger("checkConsistency")
  logger.setLevel(logging.INFO)

  total_functions = model.count("compound(")

  atoms = consistencyCheck(model,obsv,
    toggle_stable_state,toggle_sync,toggle_async)

  inconsistencies = isConsistent(atoms, toggle_stable_state, 
    toggle_sync, toggle_async, print_consistent=not benchmark_enabled)

  logger.debug("inconsistencies: \n" + str(inconsistencies))
  return total_functions, inconsistencies 

def initRepairStatsMap():
  repair_stats_map = {}
  repair_stats_map[NUM_TOTAL_FUNCTIONS] = 0
  repair_stats_map[NUM_INCONSISTENT_FUNCTIONS] = 0
  repair_stats_map[NUM_FUNC_EXTRA_REGULATORS] = 0
  repair_stats_map[AVG_EXTRA_REGULATORS] = 0
  repair_stats_map[NUM_FUNC_MISSING_REGULATORS] = 0
  repair_stats_map[AVG_MISSING_REGULATORS] = 0
  repair_stats_map[NUM_FUNC_CHANGED_SIGN] = 0
  repair_stats_map[AVG_CHANGED_SIGN] = 0
  repair_stats_map[NUM_FUNC_ALTERED_FORMAT] = 0
  repair_stats_map[AVG_ALTERED_FORMAT] = 0
  return repair_stats_map

def processFunctionRepairStats(functions, repair_stats):

  counted_extra_reg = False
  counted_missing_reg = False
  counted_sign_change = False
  counted_altered_form = False

  for atom in functions:
            
      if "missing_regulator" in atom:
        if not counted_missing_reg:
          repair_stats[NUM_FUNC_MISSING_REGULATORS] += 1
          counted_missing_reg = True
        repair_stats[AVG_MISSING_REGULATORS] += 1
        
      elif "extra_regulator" in atom:
        if not counted_extra_reg:
          repair_stats[NUM_FUNC_EXTRA_REGULATORS] += 1
          counted_extra_reg = True
        repair_stats[AVG_EXTRA_REGULATORS] += 1

      elif "sign_changed" in atom:
        if not counted_sign_change:
          repair_stats[NUM_FUNC_CHANGED_SIGN] += 1
          counted_sign_change = True
        repair_stats[AVG_CHANGED_SIGN] += 1

      elif "node_number_changes" in atom:
        node_no_variation = atom.split(')')[0].split('(')[1]
        if not counted_altered_form:
          repair_stats[NUM_FUNC_ALTERED_FORMAT] += 1
          counted_altered_form = True
        repair_stats[AVG_ALTERED_FORMAT] += int(node_no_variation)
       
      elif "missing_node_regulator" in atom or "extra_node_regulator" in atom:
        if not counted_altered_form:
          repair_stats[NUM_FUNC_ALTERED_FORMAT] += 1
          counted_altered_form = True
        repair_stats[AVG_ALTERED_FORMAT] += 1

def calculateAverages(repair_stats):
  if repair_stats[AVG_MISSING_REGULATORS] != 0:
    repair_stats[AVG_MISSING_REGULATORS] = \
      round(repair_stats[AVG_MISSING_REGULATORS] / float(repair_stats[NUM_FUNC_MISSING_REGULATORS]),1)

  if repair_stats[AVG_EXTRA_REGULATORS] != 0:
    repair_stats[AVG_EXTRA_REGULATORS] = \
      round(repair_stats[AVG_EXTRA_REGULATORS] / float(repair_stats[NUM_FUNC_EXTRA_REGULATORS]),1)
  
  if repair_stats[AVG_CHANGED_SIGN] != 0:
    repair_stats[AVG_CHANGED_SIGN] = \
      round(repair_stats[AVG_CHANGED_SIGN] / float(repair_stats[NUM_FUNC_CHANGED_SIGN]),1)

  if repair_stats[AVG_ALTERED_FORMAT] != 0:
    repair_stats[AVG_ALTERED_FORMAT] = \
      round(repair_stats[AVG_ALTERED_FORMAT] / float(repair_stats[NUM_FUNC_ALTERED_FORMAT]),1)


def repair(model, inconsistencies, repair_stats):
  timed_out_functions = ""
  unrepaired_functions = ""
  
  incst_funcs = generateInconsistentFunctions(model, inconsistencies)
  i_f_array = processInconsistentFunctions(incst_funcs)

  repair_stats[NUM_INCONSISTENT_FUNCTIONS] = len(i_f_array)

  if i_f_array:
    for func in i_f_array:
      if not benchmark_enabled: printFuncRepairStart(func)

      prev_obs = generatePreviousObservations(func, inconsistencies, toggle_sync,
        toggle_async)
      upo = processPreviousObservations(prev_obs)
      
      functions = generateFunctions(func, model, inconsistencies, upo,
        toggle_stable_state, toggle_sync, toggle_async)

      processFunctionRepairStats(functions, repair_stats)

      if functions == "timed_out": timed_out_functions += func + " "
      if functions == "no_solution": unrepaired_functions += func + " "

      if not benchmark_enabled: printRepairedLP(func, functions)
      if not benchmark_enabled: printFuncRepairEnd(func)

  calculateAverages(repair_stats)

  return timed_out_functions, unrepaired_functions


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
    for column in line:
      f.write(str(column))

      if (column != line[-1]):
        if not (column == line[-2] and line[-1] == ""):
          f.write(",\t")
       
    f.write("\n")
  f.close()

  if not benchmark_naming: logger.info("Saved benchmark to: " + str(save_path))




#-----Main-----
parseArgs()

# First, obtain the model in .lp model. If the obtained file has .bnet
# extension, it must be converted to .lp.
models = readModels()
benchmark_array = [("Model","Final State","Time Taken","Unrepairable Functions",
NUM_TOTAL_FUNCTIONS, NUM_INCONSISTENT_FUNCTIONS, 
NUM_FUNC_EXTRA_REGULATORS, AVG_EXTRA_REGULATORS,
NUM_FUNC_MISSING_REGULATORS, AVG_MISSING_REGULATORS,
NUM_FUNC_CHANGED_SIGN, AVG_CHANGED_SIGN,
NUM_FUNC_ALTERED_FORMAT, AVG_ALTERED_FORMAT)]

for model in models:
  revision_start_time = time.time()
  final_state = "consistent"
  timed_out_functions = ""
  unrepaired_functions = ""
  repair_stats = initRepairStatsMap()

  if bulk_enabled and not benchmark_enabled: print("Currently repairing model ", model[1])

  total_functions, inconsistencies = checkConsistency(model[0], obsv_path)
  repair_stats[NUM_TOTAL_FUNCTIONS] = total_functions
  
  # Second, check the consistency of the .lp model using the provided observations
  # and time step. If the model is consistent, print a message saying so.
  if inconsistencies:
    if not benchmark_enabled: print("Inconsistent model! \nRepairing...")

    # Third, if it is not, proceed with the repairs and print out the necessary ones.
    timed_out_functions, unrepaired_functions = repair(model[0], inconsistencies, repair_stats)

    if timed_out_functions or unrepaired_functions: final_state = "still inconsistent (timed out functions/no existing solutions)"
    else: final_state = "repaired"

    if not benchmark_enabled and not unrepaired_functions: print(f"Applying the above repairs to model {model[1]} will render it consistent!\n")

  revision_end_time = time.time()
  benchmark_array.append((model[1],final_state,str(revision_end_time-revision_start_time),timed_out_functions + " " + unrepaired_functions,
    repair_stats[NUM_TOTAL_FUNCTIONS], repair_stats[NUM_INCONSISTENT_FUNCTIONS],
    repair_stats[NUM_FUNC_EXTRA_REGULATORS], repair_stats[AVG_EXTRA_REGULATORS],
    repair_stats[NUM_FUNC_MISSING_REGULATORS], repair_stats[AVG_MISSING_REGULATORS],
    repair_stats[NUM_FUNC_CHANGED_SIGN], repair_stats[AVG_CHANGED_SIGN],
    repair_stats[NUM_FUNC_ALTERED_FORMAT], repair_stats[AVG_ALTERED_FORMAT]))

if benchmark_enabled:
  saveBenchmark(benchmark_array)


