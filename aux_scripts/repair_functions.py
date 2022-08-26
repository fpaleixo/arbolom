import time, clingo, re
from aux_scripts.repair_prints import printStatistics

#Path of the encodings to obtain inconsistent functions
inconsistent_functions_path = "encodings/repairs/auxiliary/inconsistent_functions.lp"

#Paths of the encodings to obtain the observations that happen before positive observations
previous_observations_sync_path = "encodings/repairs/auxiliary/previous_observations_sync.lp"
previous_observations_async_path = "encodings/repairs/auxiliary/previous_observations_async.lp"

#Paths of the encodings that generating functions
repair_encoding_stable_path = "encodings/repairs/repairs_stable.lp"
# TODO dont forge this repair_encoding_sync_path = "encodings/repairs/repairs_sync.lp"
repair_encoding_sync_path = "encodings/repairs/reworked/repairs_sync.lp"
repair_encoding_async_path = "encodings/repairs/repairs_async.lp"


#-----Functions that solve LPs with clingo-----
#Input:
# model - the model that is being revised
# inconsistencies - the inconsistencies obtained from consistency checking
# debug_mode - flag that enables extra clingo output (must remove logger in clingo.Control to see)
#Purpose: Obtains the inconsistent functions from the consistency checking phase
def generateInconsistentFunctions(model, inconsistencies, debug_mode=False, path_mode=False, enable_prints=False):
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
    
  ctl.load(inconsistent_functions_path)

  if enable_prints: print("Starting iftv generation \u23F1")
  ctl.ground([("base", [])])
  iftv = []

  with ctl.solve(yield_=True) as handle:
    for model in handle:
      iftv.append(str(model).split(" "))

  if enable_prints: print("Finished iftv generation \U0001F3C1")
  if enable_prints: printStatistics(ctl.statistics)
  return iftv

'''
#Inputs:
# func - the name of the inconsistent function
# model - the model to revise
# incst - the inconsistencies obtained from consistency checking
# upo - unique positive observations that are obtained from processPreviousObservations
# toggle_stable_state - flag that enables stable state interaction
# toggle_sync - flag that enables synchronous interaction
# toggle_async - flag that enables asynchronous interaction
# path_mode - flag that enables loading the model and inconsistencies from a file, instead of a string
# enable_prints - enables additional prints
#Purpose: Generates a function that is compatible with previously given observations, based on the obtained inconsistencies
def generateFunctions(func, model, incst, upo, toggle_stable_state, toggle_sync, toggle_async, path_mode = False, enable_prints=False):
  if enable_prints: print("Calculating optimal repairs...")

  node_number = 1
  solution_found = False
  no_timeouts = True
  functions = []
  node_limit = 1
  upo_program = ""

  if upo:
    upo_program = upo[0]
    node_limit = upo[1]

  timeout_start = time.time()
  while not solution_found and no_timeouts and node_number <= node_limit:
    clingo_args = ["0", f"-c compound={func}", f"-c node_number={node_number}"]
      
    ctl = clingo.Control(arguments=clingo_args, logger= lambda a,b: None)

    ctl.add("base", [], program=upo_program)

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

    if functions:
      solution_found = True
    elif time.time() - timeout_start > 300:
      no_timeouts = False
    else:
      node_number += 1
  
  if node_number > node_limit:
    functions = "no_solution"

  if enable_prints: print("... Done.")
  if enable_prints: printStatistics(ctl.statistics)
  return functions
'''

#Inputs:
# func - the name of the inconsistent function
# model - the model to revise
# incst - the inconsistencies obtained from consistency checking
# upo - unique positive observations that are obtained from processPreviousObservations
# toggle_stable_state - flag that enables stable state interaction
# toggle_sync - flag that enables synchronous interaction
# toggle_async - flag that enables asynchronous interaction
# path_mode - flag that enables loading the model and inconsistencies from a file, instead of a string
# enable_prints - enables additional prints
#Purpose: Generates a function that is compatible with previously given observations, based on the obtained inconsistencies
def generateFunctions(func, model, incst, upo, toggle_stable_state, toggle_sync, toggle_async, path_mode = False, enable_prints=False):
  if enable_prints: print("Calculating repairs...")

  solution_found = False
  no_timeouts = True
  functions = []
  upo_program = ""
  if upo : upo_program = upo[0]

  max_nodes, node_limit = determineMaxNodesAndLimit(func,model,upo,path_mode)

  timeout_start = time.time()
  while not solution_found and no_timeouts and max_nodes <= node_limit:
    clingo_args = ["0", f"-c compound={func}", f"-c max_node_number={max_nodes}"]
      
    ctl = clingo.Control(arguments=clingo_args, logger= lambda a,b: None)

    ctl.add("base", [], program=upo_program)

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

    if functions:
      solution_found = True
    elif time.time() - timeout_start > 300:
      no_timeouts = False
    else:
      max_nodes += 1
  
  if max_nodes > node_limit:
    functions = "no_solution"

  if enable_prints: print("... Done.")
  if enable_prints: printStatistics(ctl.statistics)
  return functions

def determineMaxNodesAndLimit(func,model,upo,path_mode):
  max_nodes = None
  node_limit = None
  original_nodes = None

  if not upo: node_limit = float('inf')
  else: node_limit = upo[1]

  f = open(model, "r")
  lines = f.readlines()
  for line in lines:
    if f"function({func}" in line:
      original_nodes = int(line.split(',')[1].split(')')[0])
      break

  max_nodes = original_nodes * 2
  if upo:
    if max_nodes > upo[1]:
      max_nodes = upo[1]

  return max_nodes, node_limit



#-----Functions that process output from clingo-----
#Input: The inconsistent functions obtained from clingo
#Purpose: Creates an array containing the name of all the inconsistent functions 
def getInconsistentFunctionsArray(inconsistent_functions):
  result = []

  for incst_func in inconsistent_functions:      
    var_name = incst_func[0].split(')')[0].split('(')[1]
    result.append(var_name)

  return result

#Input: The generated inconsistent functions output from clingo
#Purpose: Processes clingo's inconsistent functions output by creating an array with them
def processInconsistentFunctions(inconsistent_functions, enable_prints=False):
  if not inconsistent_functions:
    print("processInconsistentFunctions: No answers sets could be found	\u2755 there must be something wrong with the encoding...")

  elif inconsistent_functions[0]:

    i_f_array = getInconsistentFunctionsArray(inconsistent_functions)

    if enable_prints:
      total_iftvs = len(i_f_array)
      if(total_iftvs < 100):
        print("<Resulting inconsistent functions>")
        print(str(i_f_array),end="\n\n")
      else:
        print("Too many iftvs to print...!")
      print(f"Total iftvs: {total_iftvs}\n")

    return i_f_array

  else: 
    print("processInconsistentFunctions: No inconsistent functions could be found \u274C")



#-----Python implementation of unique positive observation determination-----
#Inputs: 
# func- the compound that has the inconsistent function
# inconsistencies - the inconsistencies obtained from consistency checking
# toggle_stable_state - flag that enables stable state interaction
# toggle_sync - flag that enables synchronous interaction
# toggle_async - flag that enables asynchronous interaction
# path_mode - flag that enables loading the inconsistencies from a file, instead of a string
#Purpose: Returns observations that happen in the timestep before
# positive observations (the observations are contained in inconsistencies)
def generatePreviousObservations(func, inconsistencies, toggle_sync, toggle_async, path_mode=False, enable_prints=False):
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

  if enable_prints: print("Calculating previous observations...")

  with ctl.solve(yield_=True) as handle:
    for model in handle:
      functions = str(model).split(" ")

  if enable_prints: print("... Done.")

  if enable_prints: printStatistics(ctl.statistics)

  if not functions[0]: #If there are no previous observations
    return []

  return functions

#Inputs: 
# -prev_obs, a string containing all previous observations
#Purpose: Returns a tuple with all unique positive observations,
# and the total number of unique positive observations
def processPreviousObservations(prev_obs, enable_prints=False):

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
  if enable_prints: print(f"Python code time for unique positive observations: {end - start}s\n")
  total_upos = len(uniques_map.values())
  return (output, total_upos)