import time
import clingo

from aux_scripts.repair_prints import printStatistics

#Path of the encodings to obtain inconsistent functions and total variables of each of those functions
iftv_path = "encodings/repairs/auxiliary/iftv.lp"

#Variables of python implementation of unique positive observations
previous_observations_sync_path = "encodings/repairs/auxiliary/previous_observations_sync.lp"
previous_observations_async_path = "encodings/repairs/auxiliary/previous_observations_async.lp"

#Paths of encodings for generating functions
repair_encoding_stable_path = "encodings/repairs/repairs_stable.lp"
repair_encoding_sync_path = "encodings/repairs/repairs_sync.lp"
repair_encoding_async_path = "encodings/repairs/repairs_async.lp"


#-----Functions that create the LPs to be used by clingo-----
#Input: The nodes generated from clingo
#Purpose: Creates a map of logic programs, indexed by inconsistent functions. Each value contains a string with the variables and total number of variables
# of the respective inconsistent function.
def getIftvsLPAndTotalVars(iftvs):
  result_LP = {}

  for iftv in iftvs:
    current_LP = ""
    var_name = ""
      
    var_name = iftv[0].split(')')[0].split('(')[1]
    
    for atom_idx in range(1, len(iftv)):
      current_LP += iftv[atom_idx] +".\n"

    result_LP[var_name] = current_LP

  return result_LP


#-----Functions that solve LPs with clingo-----
#Input: The LP containing information regarding the inconsistent functions
#Purpose: Obtains inconsistent functions, the variables and total number of variables of each function
def generateInconsistentFunctionsAndTotalVars(model, inconsistencies, debug_mode=False, path_mode=False):
  clingo_args = ["0"]
  if debug_mode:
    clingo_args.append("--output-debug=text")

  ctl = clingo.Control(arguments=clingo_args, logger= lambda a,b: None)

  if path_mode:
    ctl.load(model)
    ctl.load(inconsistencies)
  else:
    ctl.add("base", [], program=model)
    ctl.add("base", [], program=inconsistencies)
    
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
def generateFunctions(func, model, incst, upo, toggle_stable_state, toggle_sync, toggle_async, path_mode = False):
  print("Calculating optimal repairs...")
  clingo_args = ["0", f"-c compound={func}"]
    
  ctl = clingo.Control(arguments=clingo_args, logger= lambda a,b: None)

  ctl.add("base", [], program=upo)

  if path_mode:
    ctl.load(model)
    ctl.load(incst) 
  else: 
    ctl.add("base", [], program=model)
    ctl.add("base", [], program=incst)

  if toggle_stable_state:
    ctl.load(repair_encoding_stable_path)
  elif toggle_sync:
    ctl.load(repair_encoding_sync_path)
  elif toggle_async:
    ctl.load(repair_encoding_async_path)
  
  ctl.ground([("base", [])])
  functions = []

  with ctl.solve(yield_=True) as handle:
    for model in handle:
      functions = str(model).split(" ")
  
  print("... Done.")
  printStatistics(ctl.statistics)
  return functions


#-----Functions that process output from clingo-----
#Input: The generated iftv output from clingo
#Purpose: Processes clingo's iftv output by creating an LP with them, forming a map with inconsistent functions as keys and the respective
# LP containing the variables and total number of variables as value 
def processIFTVs(iftvs):
  if not iftvs:
    print("No answers sets could be found	\u2755 there must be something wrong with the encoding...")

  elif iftvs[0]:

    iftvs_LP = getIftvsLPAndTotalVars(iftvs)

    total_iftvs = len(iftvs)
    if(total_iftvs < 100):
      print("<Resulting inconsistent functions and total variables>")
      print(str(iftvs_LP),end="\n\n")
    else:
      print("Too many iftvs to print...!")
    print(f"Total iftvs: {total_iftvs}\n")

    return iftvs_LP

  else: 
    print("No iftvs could be found \u274C")



#-----Python implementation of unique positive observation determination-----
#Inputs: 
# -func, the compound that has the inconsistent function, 
# -curated_LP, the LP containing all curated observations
#Purpose: Returns observations that happen in the timestep before
# positive observations
def generatePreviousObservations(func, inconsistencies, toggle_sync, toggle_async, path_mode=False):
  print("Calculating previous observations...")
  clingo_args = ["0", f"-c compound={func}"]
  
  ctl = clingo.Control(arguments=clingo_args)

  if path_mode:
    ctl.load(inconsistencies)
  else:
    ctl.add("base", [], program=inconsistencies)

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