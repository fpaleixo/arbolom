import argparse, logging, clingo
from math import comb

#--Work in progress--
#Usage: $python repair.py -f (FILENAME) -o (OBSERVATIONS) -i (INCONSISTENCIES) -stable -sync -async -nf
#Optional flags:
#-stable -> Performs repairs using stable state observations (default).
#-sync -> Performs repairs using synchronous observations.
#-async -> Performs repairs using asynchronous observations.
#-nf -> Disables candidate function filtering (useful to obtain all candidates)
#Variables:
#FILENAME -> Path of file containing Boolean model in the BCF format written in lp.
#OBSERVATIONS -> Path of file containing observations written in lp. 
#INCONSISTENCIES -> Path of file containing inconsistencies obtained from the consistency checking phase.


#-----Testing shortcuts (to be removed at a later date)----
'''
python .\repair.py -f simple_models/lp/corrupted/3/3-corrupted-f.lp -o simple_models/lp/observations/sstate/3-obs.lp -i simple_models/lp/corrupted/3/inconsistencies/3-corrupted-f-stable_inconsistency.lp -stable
#3 variables
python .\repair.py -f simple_models/lp/corrupted/3/3-corrupted-f.lp -o simple_models/lp/observations/tseries/sync/3-obs.lp -i simple_models/lp/corrupted/3/inconsistencies/3-corrupted-f-sync_inconsistency.lp -sync
python .\repair.py -f simple_models/lp/corrupted/3/3-corrupted-f.lp -o simple_models/lp/observations/tseries/async/3-obs.lp -i simple_models/lp/corrupted/3/inconsistencies/3-corrupted-f-async_inconsistency.lp -async

python .\repair.py -f simple_models/lp/corrupted/8/8-corrupted-f.lp -o simple_models/lp/observations/sstate/8-obs.lp -i simple_models/lp/corrupted/8/inconsistencies/8-corrupted-f-stable_inconsistency.lp -stable
#5 variables
python .\repair.py -f simple_models/lp/corrupted/8/8-corrupted-f.lp -o simple_models/lp/observations/tseries/sync/8-obs.lp -i simple_models/lp/corrupted/8/inconsistencies/8-corrupted-f-sync_inconsistency.lp -sync
python .\repair.py -f simple_models/lp/corrupted/8/8-corrupted-f.lp -o simple_models/lp/observations/tseries/async/8-obs.lp -i simple_models/lp/corrupted/8/inconsistencies/8-corrupted-f-async_inconsistency.lp -async

#6 variables
python .\repair.py -f real_models/lp/corrupted/boolean_cell_cycle/boolean_cell_cycle-corrupted-f.lp -o real_models/lp/observations/tseries/sync/boolean_cell_cycle-obs.lp -i real_models/lp/corrupted/boolean_cell_cycle/inconsistencies/boolean_cell_cycle-corrupted-f-sync_inconsistency.lp -sync

#7 variables
python .\repair.py -f simple_models/lp/corrupted/11/11-corrupted-f.lp -o simple_models/lp/observations/tseries/sync/11-obs.lp -i simple_models/lp/corrupted/11/inconsistencies/11-corrupted-f-sync_inconsistency.lp -sync

#8 variables
python .\repair.py -f real_models/lp/corrupted/SP_1cell/SP_1cell-corrupted-f.lp -o real_models/lp/observations/tseries/sync/SP_1cell-obs.lp -i real_models/lp/corrupted/SP_1cell/inconsistencies/SP_1cell-corrupted-f-sync_inconsistency.lp -sync
'''


#-----Configs-----

#Command-line usage
cmd_enabled = True

#Toggle debug modes
iftv_debug_toggled = False
nodegen_debug_toggled = False
nodefilter_debug_toggled = False
edgegen_debug_toggled = False
funcgen_debug_toggled = False

#Model path
model_path = "simple_models/lp/corrupted/8/8-corrupted-f.lp"

#Paths of expected observations
obsv_path = "simple_models/lp/observations/tseries/sync/8-obs.lp"

#Paths of encodings with inconsistencies
incst_path = "simple_models/lp/corrupted/8/inconsistencies/8-corrupted-f-sync_inconsistency.lp"

#Paths of encodings for obtaining inconsistent functions and total variables of each
iftv_path = "encodings/repairs/iftv.lp"

#Paths of encodings for generating nodes
nodegen_path = "encodings/repairs/node_generator.lp"

#Paths of encodings for filtering generated nodes
ss_filternode_path = "encodings/repairs/filtering/node/ss_node_filter.lp"
sync_filternode_path = "encodings/repairs/filtering/node/sync_node_filter.lp"
async_filternode_path = "encodings/repairs/filtering/node/async_node_filter.lp"

#Paths of encodings for generating edges between nodes
edgegen_path = "encodings/repairs/edge_generator.lp"

#Path of encoding that gives node levels
node_levelgen_path = "encodings/repairs/auxiliary/node_levels.lp"

#Path of encoding that gives function levels
func_level_path = "encodings/repairs/auxiliary/function_level.lp"

#Paths of encodings for generating functions
funcgen_path = "encodings/repairs/func_generator.lp"

#Paths of encodings for filtering generated functions
ss_filter_path = "encodings/repairs/filtering/func/ss_func_filter.lp"
sync_filter_path = "encodings/repairs/filtering/func/sync_func_filter.lp"
async_filter_path = "encodings/repairs/filtering/func/async_func_filter.lp"


#Mode flags 
toggle_filtering = True
toggle_stable_state = True
toggle_sync = False
toggle_async = False


#Parser (will only be used if command-line usage is enabled above)
parser = None
args = None
if(cmd_enabled):
  parser = argparse.ArgumentParser(description="Repair an inconsistent Boolean logical model in the BCF written in lp, given a set of observations and inconsistent compounds, both written in lp.")
  parser.add_argument("-f", "--model_to_repair", help="Path to model to check the consistency of.", required=True)
  parser.add_argument("-o", "--observations_to_use", help="Path to observations obtained from the original model.", required=True)
  parser.add_argument("-i", "--inconsistencies", help="Path to inconsistencies obtained from the consistency checking phase.", required=True)
  parser.add_argument("-stable", "--stable_state", action='store_true', help="Flag to check the consistency using stable state observations (default).")
  parser.add_argument("-sync", "--synchronous", action='store_true', help="Flag to check the consistency using synchronous observations (default is stable state).")
  parser.add_argument("-async", "--asynchronous", action='store_true', help="Flag to check the consistency using asynchronous observations (default is stable state).")
  parser.add_argument("-nf", "--no_filtering", action='store_true', help="Flag to disable the filtering of function candidates (use it to obtain all candidates).")
  args = parser.parse_args()

#Global logger (change logging.(LEVEL) to desired (LEVEL) )
logging.basicConfig()
global_logger = logging.getLogger("global")
global_logger.setLevel(logging.DEBUG)



#-----Auxiliary Functions-----
#---Argument parser---
#Purpose: Parses the argument regarding which file to generate observations for.
def parseArgs():
  logger = logging.getLogger("parser")
  logger.setLevel(logging.DEBUG)

  parser = argparse.ArgumentParser(description="Repair an inconsistent Boolean logical model in the BCF written in lp, given a set of observations and inconsistent compounds, both written in lp.")
  parser.add_argument("-f", "--model_to_repair", help="Path to model to check the consistency of.", required=True)
  parser.add_argument("-o", "--observations_to_use", help="Path to observations obtained from the original model.", required=True)
  parser.add_argument("-i", "--inconsistencies", help="Path to inconsistencies obtained from the consistency checking phase.", required=True)
  parser.add_argument("-stable", "--stable_state", action='store_true', help="Flag to check the consistency using stable state observations (default).")
  parser.add_argument("-sync", "--synchronous", action='store_true', help="Flag to check the consistency using synchronous observations (default is stable state).")
  parser.add_argument("-async", "--asynchronous", action='store_true', help="Flag to check the consistency using asynchronous observations (default is stable state).")
  parser.add_argument("-nf", "--no_filtering", action='store_true', help="Flag to disable the filtering of function candidates (use it to obtain all candidates).")
  args = parser.parse_args()

  global model_path, obsv_path, incst_path, toggle_stable_state, toggle_sync, toggle_async, toggle_filtering

  model_path = args.model_to_repair
  obsv_path = args.observations_to_use
  incst_path = args.inconsistencies

  logger.debug("Obtained model: " + model_path)
  logger.debug("Obtained observations: " + obsv_path)
  logger.debug("Obtained inconsistencies: " + incst_path)


  stable = args.stable_state
  synchronous = args.synchronous
  asynchronous = args.asynchronous
  no_filtering = args.no_filtering


  if no_filtering:
    toggle_filtering = False
    logger.debug("Filtering disabled, obtaining all function candidates.")

  if stable:
    toggle_stable_state = True
    toggle_sync = False
    toggle_async = False
    logger.debug("Mode used: Stable State \U0001f6d1")

  elif synchronous:
    toggle_stable_state = False
    toggle_sync = True
    toggle_async = False
    logger.debug("Mode used: Synchronous \U0001f550")

  elif asynchronous:
    toggle_stable_state = False
    toggle_sync = False
    toggle_async = True
    logger.debug("Mode used: Asynchronous \U0001f331")

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

#Purpose: Prints the initial node generation phase message
def printFuncRepairStart(current_function):
  print(f"\033[1;32m ----{current_function} REPAIR START----\033[0;37;40m")

#Purpose: Prints the initial node generation phase message
def printFuncRepairEnd(current_function):
  print(f"\033[1;32m ----{current_function} REPAIR END----\033[0;37;40m")

#Purpose: Prints the initial iftv generation phase message
def printIFTVStart():
  print("\033[1;32m ----IFTV GENERATION START----\033[0;37;40m")

#Purpose: Prints the final iftv generation phase message
def printIFTVEnd():
  print("\033[1;32m ----IFTV GENERATION END----\033[0;37;40m")

#Purpose: Prints the initial node generation phase message
def printNodeStart():
  print("\033[1;32m ----NODE GENERATION START----\033[0;37;40m")

#Purpose: Prints the final node generation phase message
def printNodeEnd():
  print("\n\033[1;32m ----NODE GENERATION END----\033[0;37;40m\n")

#Purpose: Prints the initial node filter phase message
def printNodeFilterStart():
  print("\033[1;32m ----NODE FILTER START----\033[0;37;40m")

#Purpose: Prints the final node filter phase message
def printNodeFilterEnd():
  print("\n\033[1;32m ----NODE FILTER END----\033[0;37;40m\n")

#Purpose: Prints the initial edge generation phase message
def printEdgeStart():
  print("\033[1;32m ----EDGE GENERATION START----\033[0;37;40m")

#Purpose: Prints the final edge generation phase message
def printEdgeEnd():
  print("\n\033[1;32m ----EDGE GENERATION END----\033[0;37;40m\n")

#Purpose: Prints the initial function generation phase message
def printFuncStart():
  print("\033[1;32m ----FUNCTION GENERATION START----\033[0;37;40m")

#Purpose: Prints the final function generation phase message
def printFuncEnd():
  print("\n\033[1;32m ----FUNCTION GENERATION END----\033[0;37;40m")



#-----Functions that create the LPs to be used by clingo-----

#Purpose: Separates the inconsistencies from the curated observations that are outputted from the consistency checking phase
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
#Purpose: Creates the logic program that will be used to create nodes
def getIftvsLP(iftvs):
  result_LP = {}

  for iftv in iftvs:
    current_LP = ""
    var_name = ""
    for atom in iftv:

      if "inconsistent_function" in atom:
        var_name = iftv[0].split(')')[0].split('(')[1]
      else:
        current_LP += atom +".\n"

    result_LP[var_name] = current_LP
  return result_LP

#Input: The nodes generated from clingo
#Purpose: Creates the logic program that will be used to establish relations between nodes
def getNodesLP(nodes):
  result_LP = ""
  current_node_id = 1
  
  for node in nodes:
    result_LP += f"node_({current_node_id}).\n"

    for variable in node:
      var_name = variable.split(')')[0].split('(')[1]
      result_LP += f"node_variable({current_node_id},{var_name}).\n"
    
    result_LP += "\n"
    current_node_id += 1

  return result_LP

#Input: The nodes filtered from clingo
#Purpose: Creates the logic program containing those nodes
def getFilteredNodesLP(nodes):
  result_LP = ""
  
  for node in nodes:
    result_LP += node[0].split("filtered_")[1] + ".\n"

    for variable in node[1:]:
      result_LP += variable.split("filtered_")[1] + ".\n"
    result_LP += "\n"

  return result_LP

#Input: The edges generated from clingo
#Purpose: Creates the logic program that will be used to create function candidates
def getEdgesLP(edges):
  result_LP = ""
  
  for edge in edges[0]:
    result_LP += edge + ".\n"

  return result_LP

#Input: Inconsistent function
#Purpose: Extracts from the original model everything except the part where the inconsistent regulatory function func is defined
def getOriginalModelLP(func):
  original = open(model_path, 'r')
  lines = original.readlines()
  original_LP = ""
  inconsistent_func_LP = ""

  for line in lines: 
    if f"function({func}" not in line and f"term({func}" not in line:
      original_LP += line
    else:
      inconsistent_func_LP += line

  return original_LP, inconsistent_func_LP



#-----Functions that process output from clingo-----
#Input: The generated iftv output from clingo
#Purpose: Processes clingo's iftv output by creating an LP with them, forming a map with inconsistent functions as keys and the respective
#LP containing the variables and total number of variables as value 
def processIFTVs(iftvs):
  if not iftvs:
    print("No answers sets could be found	\u2755 there must be something wrong with the encoding...")

  elif iftvs[0]:

    iftvs_LP = getIftvsLP(iftvs)

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

#Input: The generated nodes output from clingo
#Purpose: Processes clingo's node generation output by creating an LP with them, identifying each node
def processNodes(nodes):
  if not nodes:
    print("No answers sets could be found	\u2755 there must be something wrong with the encoding...")

  elif nodes[0]:

    nodes_LP = getNodesLP(nodes)

    total_nodes = len(nodes)
    if(total_nodes < 100):
      print("<Resulting nodes>")
      print(nodes_LP,end="")
    else:
      print("Too many nodes to print...!")
    print(f"Total nodes: {total_nodes}")

    return nodes_LP

  else: 
    print("No nodes could be found \u274C")

#Input: The generated nodes output from clingo
#Purpose: Processes clingo's node generation output by creating an LP with them, identifying each node
def processFilteredNodes(nodes):
  if not nodes:
    print("No answers sets could be found	\u2755 there must be something wrong with the encoding...")

  elif nodes[0]:

    nodes_LP = getFilteredNodesLP(nodes)

    total_nodes = len(nodes)
    if(total_nodes < 100):
      print("<Filtered nodes>")
      print(nodes_LP,end="")
    else:
      print("Too many nodes to print...!")
    print(f"Total nodes: {total_nodes}")

    return nodes_LP

  else: 
    print("All nodes were filtered out... \u274C")

#Input: The generated edges output from clingo
#Purpose: Processes clingo's edge generation output by creating an LP with them
def processEdges(edges):
  if not edges:
    print("No answers sets could be found	\u2755 there must be something wrong with the encoding...")

  elif edges[0]:

    edges_LP = getEdgesLP(edges)

    total_edges = len(edges[0])
    if(total_edges < 100):
      print("<Resulting edges>")
      print(edges_LP)
    else:
      print("Too many edges to print...!")
    print(f"Total edges: {total_edges}")

    return edges_LP

  else: 
    print("No edges could be found \u274C")

#Input: The function candidates output from clingo
#Purpose: Processes clingo's function candidates output by creating a map with it and printing it
def processFunctions(functions):
  if not functions:
    print("No answers sets could be found	\u2755 there must be something wrong with the encoding...")

  elif functions[0]:

    total_candidates = len(functions)

    print("<Resulting candidates>")
    if(total_candidates < 500):
      
      for candidate_idx in range(0,total_candidates):
        organized_candidates = {}
        current_candidate = functions[candidate_idx]
        
        print(f"Candidate {candidate_idx + 1}: ")

        for atom in current_candidate:

          if "function" in atom:
            print(atom)
          
          elif "term" in atom:
            term_number = atom.split(',')[1]

            if term_number not in organized_candidates.keys():
              organized_candidates[term_number] = [atom]
            else:
              organized_candidates[term_number].append(atom)
            
        for term_no in organized_candidates.keys():
          for term in organized_candidates[term_no]:
            print(term)
        print()
    else:
      print("Too many candidates to print...!")
    print(f"Total candidates: {total_candidates}")

  else: 
    print("No function candidates could be found \u274C") 



#-----Level search functions-----
#TODO Inputs:
#TODO Purpose:
def findLevelCandidates(level):
  generateLevelCandidatesTest(level)
  #TODO

#Inputs: A level, represented by an array of integers ordered in decreasing order
#Purpose: Find the index of the clause with the lowest number of missing variables
def findIdxOfLowestClause(level):
  for idx in range(1, len(level)):
    if level[idx] < level[idx-1]:
      return idx
  
  return 0 #if all clauses have the same value, return the index of the first clause


#Inputs: A level, represented by an array of integers ordered in decreasing order, and the total number of variables to consider
#Purpose: Takes a level and tries to find the next existing level
def getNextLevel(level, total_variables):
  if level == None: return None

  current_level = level.copy()
  exists = False

  while not exists:
    add_clause = current_level.copy()
    add_clause.append(1) #start by calculating the next level by trying to add a new clause with 1 missing variable
    exists = generateLevelCandidatesTest(add_clause)

    #if that level does not exist but the second last clause has more than 1 missing variable, try to incrementally approach the new clause's 
    #number of missing variables to that number
    while not exists and add_clause[-1] < add_clause[-2]:  
        add_clause[-1] += 1
        exists = generateLevelCandidatesTest(add_clause)

    if exists:
      return add_clause
    
    else: #if adding a new clause did not produce an existing level, then try to increment the level of an existing clause
      if not exists: 
        clause_to_increase_idx = findIdxOfLowestClause(current_level)

        next_level = current_level[:clause_to_increase_idx + 1] #copy everything from the first clause to the clause to be incremented
        next_level[clause_to_increase_idx] += 1

        current_level = next_level
        if current_level[0] == total_variables: #if the first clause has as many missing variables as the number of total variables, then we have exhausted all levels
          return None

        exists = generateLevelCandidatesTest(current_level)

  return current_level

#Inputs: A level, represented by an array of integers ordered in decreasing order, and the total number of variables to consider
#Purpose: Takes a level and tries to find the previous existing level
def getPreviousLevel(level, total_variables):
  if level == [0] or level == None: return None

  current_level = level.copy()
  exists = False

  while not exists:
    remove_clause = current_level.copy()
    
    #start by calculating the previous level by trying to remove the last clause if it has only 1 missing variable
    if remove_clause[-1] == 1:
      remove_clause.pop()

      if len(remove_clause) == 1 and remove_clause[0] == 1: #if we only have one clause left and that clause has level 1, then we've reached the last level
        exists = generateLevelCandidatesTest([0])
        if not exists:
          return None
        else:
          return [0]

      exists = generateLevelCandidatesTest(remove_clause)

      if exists:
        return remove_clause
      
      else:
        current_level = remove_clause

    else: #if we were unable to remove the last clause, then decrease its level

      current_level[-1] -= 1
      #add the maximum amount of clauses with the level of the new lowest clause
      #TODO perhaps implement a binary search of sorts, to avoid always exploring everything?
      max_clauses = comb(total_variables, total_variables - current_level[0])

      while len(current_level) != max_clauses:
        current_level.append(current_level[-1])

      exists = generateLevelCandidatesTest(current_level)

  return current_level


#TODO Inputs:
#Purpose: Search for a viable candidate using function levels
def levelSearch(func_level, nodes_LP, node_levels_LP):

  found_candidates = False
  next_level = func_level
  previous_level = func_level

  while not found_candidates:
    
    if next_level == previous_level: #first iteration
      candidates = generateLevelCandidatesTest(True)
    
    else :
      candidates = findLevelCandidates(next_level)

      if not candidates:
        candidates = findLevelCandidates(previous_level)

    if candidates:
      found_candidates = candidates
    else:
      next_level = getNextLevel(next_level)
      previous_level = getPreviousLevel(previous_level)

  return found_candidates



#-----Functions that solve LPs with clingo-----
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

#Purpose: Generates all nodes containing the possible variable conjunctions
def generateNodes(iftvs_LP):
  clingo_args = ["0"]
  if nodegen_debug_toggled:
    clingo_args.append("--output-debug=text")

  ctl = clingo.Control(arguments=clingo_args)

  ctl.load(model_path)
  ctl.load(nodegen_path)
  ctl.add("base",[],program=iftvs_LP)

  print("Starting node generation \u23F1")
  ctl.ground([("base", [])])
  nodes = []

  with ctl.solve(yield_=True) as handle:
    for model in handle:
      nodes.append(str(model).split(" "))

  print("Finished node generation \U0001F3C1")
  printStatistics(ctl.statistics)
  return nodes

#Inputs: The compound with the inconsistent function and the LPs with the original functions minus the inconsistent function, and the generated nodes
#Purpose: Filters out nodes that produce 1s when 0s are expected
def filterNodes(func, incst_LP, original_LP, nodes_LP):
  clingo_args = ["0", f"-c compound={func}"]
  if nodefilter_debug_toggled:
    clingo_args.append("--output-debug=text")

  ctl = clingo.Control(arguments=clingo_args)

  ctl.add("base", [], program=incst_LP)
  ctl.add("base", [], program=original_LP)
  ctl.add("base",[], program=nodes_LP)

  if toggle_stable_state:
    ctl.load(ss_filternode_path)
  elif toggle_sync:
    ctl.load(sync_filternode_path)
  elif toggle_async:
    ctl.load(async_filternode_path)

  print("Starting node filtering \u23F1")
  ctl.ground([("base", [])])
  nodes = []

  with ctl.solve(yield_=True) as handle:
    for model in handle:
      nodes.append(str(model).split(" "))

  print("Finished node filtering \U0001F3C1")
  printStatistics(ctl.statistics)
  return nodes

#Purpose: Generates edges between nodes
def generateEdges(nodes_LP):
  clingo_args = ["0"]
  if edgegen_debug_toggled:
    clingo_args.append("--output-debug=text")

  ctl = clingo.Control(arguments=clingo_args)

  ctl.load(edgegen_path)
  ctl.add("base",[],program=nodes_LP)

  print("Starting edge generation \u23F1")
  ctl.ground([("base", [])])
  edges = []

  with ctl.solve(yield_=True) as handle:
    for model in handle:
      edges.append(str(model).split(" "))

  print("Finished edge generation \U0001F3C1")
  printStatistics(ctl.statistics)
  return edges

#Input: The logic programs containing the number of total variables, and the generated nodes
#Purpose: Returns the level of each generated node
def generateNodeLevels(iftvs_LP, nodes_LP):
  clingo_args = ["0"]
    
  ctl = clingo.Control(arguments=clingo_args)

  ctl.add("base", [], program=iftvs_LP)
  ctl.add("base", [], program=nodes_LP)
  ctl.load(node_levelgen_path)
  

  ctl.ground([("base", [])])
  levels = []

  with ctl.solve(yield_=True) as handle:
    for model in handle:
      levels.append(str(model).split(" "))
  
  return levels

#Inputs: The logic programs containing the number of total variables, and the function to determine the level of
#Purpose: Returns the level of the given function
def generateFuncLevel(iftvs_LP, func_LP):
  clingo_args = ["0"]
    
  ctl = clingo.Control(arguments=clingo_args)

  ctl.add("base", [], program=iftvs_LP)
  ctl.add("base", [], program=func_LP)
  ctl.load(func_level_path)

  ctl.ground([("base", [])])
  levels = []

  with ctl.solve(yield_=True) as handle:
    for model in handle:
      levels.append(str(model).split(" "))
  
  return levels

#Inputs: Level to test
#Purpose: Used to test if level traversal is working as expected
def generateLevelCandidatesTest(level):
  candidates = []
  ''' 4 vars  
  candidates.append([0])
  candidates.append([1,1])
  candidates.append([1,1,1])
  candidates.append([1,1,1,1])
  candidates.append([2,1])
  candidates.append([2,1,1])
  candidates.append([2,2])
  candidates.append([2,2,1])
  candidates.append([2,2,2])
  candidates.append([2,2,2,2])
  candidates.append([2,2,2,2,2])
  candidates.append([2,2,2,2,2,2])
  candidates.append([3,1])
  candidates.append([3,2,2])
  candidates.append([3,2,2,2])
  candidates.append([3,3,2])
  candidates.append([3,3,3,3])
  '''

  '''3 vars'''
  candidates.append([0])
  candidates.append([1,1])
  candidates.append([1,1,1])
  candidates.append([2,1])
  candidates.append([2,2,2])


  if level in candidates:
    return True
  else:
    return False

#Input: The logic program containing information regarding the terms that can be used to create function candidates
#Purpose: Generates all possible function candidates with the given logic progam
def generateFunctions(original_LP,func,curated_LP,iftv_LP,nodes_LP,edges_LP):
  clingo_args = ["0", f"-c compound={func}"]
  if funcgen_debug_toggled:
    clingo_args.append("--output-debug=text")
    
  ctl = clingo.Control(arguments=clingo_args)

  ctl.add("base", [], program=original_LP)
  ctl.add("base", [], program=curated_LP)
  ctl.add("base", [], program=iftv_LP)
  ctl.add("base", [], program=nodes_LP)
  ctl.add("base", [], program=edges_LP)
  ctl.load(funcgen_path)

  if toggle_filtering:
    if toggle_stable_state:
      ctl.load(ss_filter_path)
    elif toggle_sync:
      ctl.load(sync_filter_path)
    elif toggle_async:
      ctl.load(async_filter_path)

  print("Starting function generation \u23F1")
  ctl.ground([("base", [])])
  functions = []

  with ctl.solve(yield_=True) as handle:
    for model in handle:
      functions.append(str(model).split(" "))
  
  print("Finished function generation \U0001F3C1")
  printStatistics(ctl.statistics)
  return functions



#-----Main-----
'''
level = [2,2,2]
for i in range(0,16):
  #level = getNextLevel(level,4)
  level = getPreviousLevel(level,3)
  print(level)
'''

if cmd_enabled:
  parseArgs()

printIFTVStart()
incst_LP, curated_LP = getInconsistenciesAndCuratedLP()

iftvs = generateInconsistentFunctionsAndTotalVars(incst_LP)
processed_ifts_output = processIFTVs(iftvs)
printIFTVEnd()

if processed_ifts_output:
  for func in processed_ifts_output.keys():

    printFuncRepairStart(func)

    original_LP = getOriginalModelLP(func)

    printNodeStart()
    nodes = generateNodes(processed_ifts_output[func])
    process_nodes_output = processNodes(nodes)
    printNodeEnd()

    if process_nodes_output:

      if toggle_filtering:
        printNodeFilterStart()
        filtered_nodes = filterNodes(func, curated_LP, original_LP[0], process_nodes_output)
        process_nodes_output = processFilteredNodes(filtered_nodes)
        printNodeFilterEnd()

      printEdgeStart()
      edges = generateEdges(process_nodes_output)
      process_edges_output = processEdges(edges)
      printEdgeEnd()

      if process_edges_output:
        printFuncStart()
        node_levels_LP = generateNodeLevels(processed_ifts_output[func], process_nodes_output)
        func_level_LP = generateFuncLevel(processed_ifts_output[func], original_LP[1])
        print(node_levels_LP)
        print(func_level_LP)
        functions = generateFunctions(original_LP[0], func, curated_LP,
          processed_ifts_output[func], process_nodes_output, process_edges_output)
        process_functions_output = processFunctions(functions)
        printFuncEnd()

    printFuncRepairEnd(func)
  
