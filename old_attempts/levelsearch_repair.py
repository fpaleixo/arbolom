import argparse, logging, clingo, time
from aux_scripts.repair_prints import *
from aux_scripts.level_search import *
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
python .\old_attempts/levelsearch_repair.py-f simple_models/lp/corrupted/3/3-corrupted-f.lp -o simple_models/lp/observations/sstate/3-obs.lp -i simple_models/lp/corrupted/3/inconsistencies/3-corrupted-f-stable_inconsistency.lp -stable
#3 variables
python old_attempts/levelsearch_repair.py -f simple_models/lp/corrupted/3/3-corrupted-f.lp -o simple_models/lp/observations/tseries/sync/3-obs.lp -i simple_models/lp/corrupted/3/inconsistencies/3-corrupted-f-sync_inconsistency.lp -sync
python old_attempts/levelsearch_repair.py -f simple_models/lp/corrupted/3/3-corrupted-f.lp -o simple_models/lp/observations/tseries/async/3-obs.lp -i simple_models/lp/corrupted/3/inconsistencies/3-corrupted-f-async_inconsistency.lp -async

python old_attempts/levelsearch_repair.py -f simple_models/lp/corrupted/8/8-corrupted-f.lp -o simple_models/lp/observations/sstate/8-obs.lp -i simple_models/lp/corrupted/8/inconsistencies/8-corrupted-f-stable_inconsistency.lp -stable
#5 variables
python old_attempts/levelsearch_repair.py -f simple_models/lp/corrupted/8/8-corrupted-f.lp -o simple_models/lp/observations/tseries/sync/8-obs.lp -i simple_models/lp/corrupted/8/inconsistencies/8-corrupted-f-sync_inconsistency.lp -sync
python old_attempts/levelsearch_repair.py -f simple_models/lp/corrupted/8/8-corrupted-f.lp -o simple_models/lp/observations/tseries/async/8-obs.lp -i simple_models/lp/corrupted/8/inconsistencies/8-corrupted-f-async_inconsistency.lp -async

#6 variables
python old_attempts/levelsearch_repair.py -f real_models/lp/corrupted/boolean_cell_cycle/boolean_cell_cycle-corrupted-f.lp -o real_models/lp/observations/tseries/sync/boolean_cell_cycle-obs.lp -i real_models/lp/corrupted/boolean_cell_cycle/inconsistencies/boolean_cell_cycle-corrupted-f-sync_inconsistency.lp -sync

#7 variables
python old_attempts/levelsearch_repair.py -f simple_models/lp/corrupted/11/11-corrupted-f.lp -o simple_models/lp/observations/tseries/sync/11-obs.lp -i simple_models/lp/corrupted/11/inconsistencies/11-corrupted-f-sync_inconsistency.lp -sync

#8 variables
python old_attempts/levelsearch_repair.py -f real_models/lp/corrupted/SP_1cell/SP_1cell-corrupted-f.lp -o real_models/lp/observations/tseries/sync/SP_1cell-obs.lp -i real_models/lp/corrupted/SP_1cell/inconsistencies/SP_1cell-corrupted-f-sync_inconsistency.lp -sync


NO SOLUTIONS
#5 variables
python .\repair.py -f simple_models/lp/corrupted/8/8-corrupted-f-nosol.lp -o simple_models/lp/observations/tseries/sync/8-obs.lp -i simple_models/lp/corrupted/8/inconsistencies/8-corrupted-f-nosol-sync_inconsistency.lp -sync

#6 variables
python .\repair.py -f real_models/lp/corrupted/boolean_cell_cycle/boolean_cell_cycle-corrupted-f-nosol.lp -o real_models/lp/observations/tseries/sync/boolean_cell_cycle-obs.lp -i real_models/lp/corrupted/boolean_cell_cycle/inconsistencies/boolean_cell_cycle-corrupted-f-nosol-sync_inconsistency.lp -sync

#7 variables
python .\repair.py -i simple_models/lp/corrupted/11/inconsistencies/11-corrupted-f-nosol-sync_inconsistency.lp -o simple_models/lp/observations/tseries/sync/11-obs.lp -f simple_models/lp/corrupted/11/11-corrupted-f-nosol.lp -sync

#8 variables
python .\repair.py -f real_models/lp/corrupted/SP_1cell/SP_1cell-corrupted-f-nosol.lp -o real_models/lp/observations/tseries/sync/SP_1cell-obs.lp -i real_models/lp/corrupted/SP_1cell/inconsistencies/SP_1cell-corrupted-f-nosol-sync_inconsistency.lp -sync
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
iftv_path = "old_attempts/encodings/repairs/levelsearch/iftv.lp"

#Paths of encodings for generating nodes
nodegen_path = "old_attempts/encodings/repairs/levelsearch/node_generator.lp"

#Paths of encodings for filtering generated nodes
ss_filternode_path = "old_attempts/encodings/repairs/levelsearch/filtering/node/ss_node_filter.lp"
sync_filternode_path = "old_attempts/encodings/repairs/levelsearch/filtering/node/sync_node_filter.lp"
async_filternode_path = "old_attempts/encodings/repairs/levelsearch/filtering/node/async_node_filter.lp"

#Paths of encodings for generating edges between nodes
edgegen_path = "old_attempts/encodings/repairs/levelsearch/edge_generator.lp"

#Path of encoding that gives node levels
node_levelgen_path = "old_attempts/encodings/repairs/levelsearch/auxiliary/node_levels.lp"

#Path of encoding that gives function levels
func_level_path = "old_attempts/encodings/repairs/levelsearch/auxiliary/function_level.lp"

#Paths of encodings for generating functions
funcgen_path = "old_attempts/encodings/repairs/levelsearch/func_generator.lp"

#Paths of encodings for filtering generated functions
ss_filter_path = "old_attempts/encodings/repairs/levelsearch/filtering/func/ss_func_filter.lp"
sync_filter_path = "old_attempts/encodings/repairs/levelsearch/filtering/func/sync_func_filter.lp"
async_filter_path = "old_attempts/encodings/repairs/levelsearch/filtering/func/async_func_filter.lp"

#Mode flags 
toggle_filtering = True
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

#Variables for statistics
levels_searched = 0
clingo_cumulative_level_search_time = 0


#-----Auxiliary Functions-----
#---Argument parser---
#Purpose: Parses the arguments of function repair
def parseArgs():
  logger = logging.getLogger("parser")
  logger.setLevel(logging.DEBUG)

  global parser, args

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


#---LP combiner---
#Input: An array of strings, where each string is an LP
#Purpose: Combines the LPs in the array into a single string (to avoid having to pass many LPs as different arguments)
def combineLPs(LP_array):
  resulting_LP = ""
  for LP in LP_array:
    resulting_LP += LP + "\n"
  return resulting_LP


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

#Input: The nodes generated from clingo
#Purpose: Creates a logic program containing information about nodes (specifically, ID and variables contained within)
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
#Purpose: Creates a logic program containing those filtered nodes
def getFilteredNodesLP(nodes):
  result_LP = ""
  
  for node in nodes:
    result_LP += node[0].split("filtered_")[1] + ".\n"

    for variable in node[1:]:
      result_LP += variable.split("filtered_")[1] + ".\n"
    result_LP += "\n"

  return result_LP

#Input: The edges generated from clingo
#Purpose: Creates a logic program using the edge predicate, which connects nodes to other nodes that contain them
def getEdgesLP(edges):
  result_LP = ""
  
  for edge in edges[0]:
    result_LP += edge + ".\n"

  return result_LP

#Input: Inconsistent function
#Purpose: Extracts everything from the original model except the part where the inconsistent regulatory function func is defined
# (so that clingo can use that original model with the candidate functions it generates)
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

#Input: Node levels, as outputted from clingo
#Purpose: Transforms clingo's output into an LP
def getNodeLevelsLP(node_levels):
  node_levels_LP = ""

  for level in node_levels[0]:
    node_levels_LP += level + ".\n"

  return node_levels_LP

#Input: Level in array format
#Purpose: Takes a level in array format and produces a logic program from it
def getLevelLP(level):
  clause_levels_LP = ""

  for clause_idx in range(0, len(level)):
    clause_levels_LP += f"clause_level({clause_idx + 1}, {level[clause_idx]}).\n" 

  return clause_levels_LP


#-----Level search functions-----
#Inputs: A level, represented by an array of integers ordered in decreasing order, 
# the LP containing base information for level search, and the total number of variables to consider
#Purpose: Takes a level and tries to find the next existing level
def getNextLevel(level, level_search_base_LP, total_variables):
  if level == None: return None

  global levels_searched

  current_level = level.copy()

  if current_level == [0]: #level [0] always has [1,1] as next level
      current_level = [1]

  exists = False

  max_clauses = comb(total_variables, total_variables - current_level[0])
     
  while not exists:
    if(len(current_level) != max_clauses):
      current_level.append(1) #start by calculating the next level by trying to add a new clause with 1 missing variable
      exists = generateLevelCandidates(level_search_base_LP, getLevelLP(current_level))
      levels_searched += 1

    if exists:
      return current_level
    
    else: #if adding a new clause did not produce an existing level, then try to increment the level of an existing clause
      if not exists: 
        clause_to_increase_idx = findIdxOfLowestClause(current_level)

        if clause_to_increase_idx == 0: #if we're increasing the first clause
          next_level = [current_level[0] + 1]
          current_level = next_level

          if current_level[0] == total_variables: #if the first clause has as many missing variables as the number of total variables, then we have exhausted all levels
            return None

          max_clauses = comb(total_variables, total_variables - current_level[0])
        
        else:
          next_level = current_level[:clause_to_increase_idx + 1] #copy everything from the first clause to the clause to be incremented
          next_level[clause_to_increase_idx] += 1

          current_level = next_level

          exists = generateLevelCandidates(level_search_base_LP, getLevelLP(current_level))
          levels_searched += 1

  return current_level

#Inputs: level, the level obtained from lowering the last term's number of missing variables to 1, the LP containing base information for level search, and the total number of variables
#Purpose: Calculates what the highest level is taking the given level as a starting point, using a binary search
def getLevelBinarySearch(level, level_search_base_LP, total_variables):

  global levels_searched

  minimum_level = level.copy()
  maximum_level = minimum_level.copy()
  base_term_number = len(level) - 1 #number of terms before the last term

  max_clauses = comb(total_variables, total_variables - maximum_level[0])

  while len(maximum_level) != max_clauses:
    maximum_level.append(maximum_level[-1])

  exists = generateLevelCandidates(level_search_base_LP, getLevelLP(minimum_level))
  levels_searched += 1

  if not exists: #if the smallest level possible doesn't exist, return the minimum and exists = False
    return minimum_level, False

  previous_min = None
  previous_max = None
  minimum_term_number = len(minimum_level) - base_term_number
  maximum_term_number = len(maximum_level) - base_term_number
  mid_level = None

  while previous_min != minimum_term_number or previous_max != maximum_term_number: #while there are still changes

    mid_term_number = round((maximum_term_number + minimum_term_number) / 2)

    total_mid_terms = base_term_number + mid_term_number
    mid_level = maximum_level[:total_mid_terms]

    exists = generateLevelCandidates(level_search_base_LP, getLevelLP(mid_level))
    levels_searched += 1

    previous_min = minimum_term_number
    previous_max = maximum_term_number
    if exists: #minimum needs to be raised
      minimum_term_number = mid_term_number

    else: #maximum needs to be lowered
      maximum_term_number = mid_term_number
  
  return mid_level, exists

#Inputs: A level, represented by an array of integers ordered in decreasing order, 
# the LP containing base information for level search, and the total number of variables to consider
#Purpose: Takes a level and tries to find the previous existing level
def getPreviousLevel(level, level_search_base_LP, total_variables):
  if level == [0] or level == None: return None

  global levels_searched

  current_level = level.copy()
  exists = False

  while not exists:
    remove_clause = current_level.copy()
    
    #start by calculating the previous level by trying to remove the last clause if it has only 1 missing variable
    if remove_clause[-1] == 1 and len(remove_clause) != 1: #if the length is 1, we're at level [1] and thus should go to [0]
      remove_clause.pop()

      if len(remove_clause) == 1 and remove_clause[0] == 1: #if we only have one clause left and that clause has level 1, then we've reached the last level
        exists = generateLevelCandidates(level_search_base_LP, getLevelLP([0]))
        levels_searched += 1

        if not exists:
          return None
        else:
          return [0]
      
      exists = generateLevelCandidates(level_search_base_LP, getLevelLP(remove_clause))
      levels_searched += 1

      if exists:
        return remove_clause
      
      else:
        current_level = remove_clause

    else: #if we were unable to remove the last clause, then decrease its level
      
      current_level[-1] -= 1
      #add the maximum amount of clauses with the level of the new lowest clause
      max_clauses = comb(total_variables, total_variables - current_level[0])

      if max_clauses != len(current_level) and current_level[-1] == 1:
        current_level, exists = getLevelBinarySearch(current_level, level_search_base_LP, total_variables)

      else: 
        while len(current_level) != max_clauses:
          current_level.append(current_level[-1])

        exists = generateLevelCandidates(level_search_base_LP, getLevelLP(current_level))
        levels_searched += 1

  return current_level


#Inputs: The compound whose function is inconsistent, the level of that function, the total number of variables to consider,
# an LP with the original LP, the curated observations, and the LP containing base information for level search
#Purpose: Search for a viable candidate using function levels
def levelSearch(func, func_level, total_variables, original_LP, curated_LP, level_search_base_LP):

  found_candidates = None
  found_candidates_level = None
  next_level = func_level
  previous_level = func_level

  while not found_candidates:
    
    if next_level == previous_level: #first iteration
      found_candidates = generateLevelCandidates(level_search_base_LP, getLevelLP(next_level), func, original_LP, curated_LP, all_candidates=True)
      found_candidates_level = next_level

    else:
      if next_level:
        found_candidates = generateLevelCandidates(level_search_base_LP, getLevelLP(next_level), func, original_LP, curated_LP, all_candidates=True)
        found_candidates_level = next_level

      if not found_candidates and previous_level:
        found_candidates = generateLevelCandidates(level_search_base_LP, getLevelLP(previous_level), func, original_LP, curated_LP, all_candidates=True)
        found_candidates_level = previous_level

    if not found_candidates:
      
      next_level = getNextLevel(next_level, level_search_base_LP, total_variables)
      previous_level = getPreviousLevel(previous_level, level_search_base_LP, total_variables)

      #print("Trying next level: ", next_level)
      #print("Trying previous level: ", previous_level )
      #print()

      if next_level == None and previous_level == None: #If we have run out of levels, no candidates could be found
        return None

  return found_candidates, found_candidates_level



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
#Purpose: Processes clingo's function candidates output by printing them in a more readable manner
def processFunctions(functions):
  if not functions:
    print("No answers sets could be found	\u2755 there must be something wrong with the encoding...")

  elif functions[0]:

    total_candidates = len(functions)

    print("<Resulting candidates>")
    if(total_candidates < 500):
      
      for candidate_idx in range(0,total_candidates):
        current_candidate = functions[candidate_idx]
        
        print(f"Candidate {candidate_idx + 1}: ")

        for atom in current_candidate:

          if "function" in atom:
            print(atom)
        
        print()

    else:
      print("Too many candidates to print...!")
    print(f"Total candidates: {total_candidates}\n")

  else: 
    print("No function candidates could be found \u274C") 



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

#Inputs: The compound with the inconsistent function and the LPs with the curated observations,
# the original functions minus the inconsistent function, and the generated nodes
#Purpose: Filters out nodes that produce 1s when 0s are expected (using these nodes in functions would be guaranteed)
# to produce wrong results)
def filterNodes(func, curated_LP, original_LP, nodes_LP):
  clingo_args = ["0", f"-c compound={func}"]
  if nodefilter_debug_toggled:
    clingo_args.append("--output-debug=text")

  ctl = clingo.Control(arguments=clingo_args)

  ctl.add("base", [], program=curated_LP)
  ctl.add("base", [], program=original_LP)
  ctl.add("base", [], program=nodes_LP)

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

#Input: The generated nodes LP
#Purpose: Generates edges between nodes
def generateEdges(nodes_LP):
  clingo_args = ["0"]
  if edgegen_debug_toggled:
    clingo_args.append("--output-debug=text")

  ctl = clingo.Control(arguments=clingo_args)

  ctl.load(edgegen_path)
  ctl.add("base", [], program=nodes_LP)

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

#Inputs: LPs containing the base information that level search requires, the desired levelof function to generate,
# and (optionally, if all candidates are to be generated) the inconsistent compound, the original model minus that compound's function,
# the curated observations and, lastly, a boolean specifying whether all candidates are to be generated or not  
#Purpose: Creates function candidates with the same level as level_LP
def generateLevelCandidates(level_search_base_LP, level_LP, func=None, original_LP=None, curated_LP=None, all_candidates=False):
  clingo_args = []

  if all_candidates:
    clingo_args = ["0", f"-c compound={func}"]
    
  ctl = clingo.Control(arguments=clingo_args)

  ctl.add("base", [], program=level_search_base_LP)
  ctl.add("base", [], program=level_LP)
  ctl.load(funcgen_path)

  if all_candidates:
    ctl.add("base", [], program=original_LP)
    ctl.add("base", [], program=curated_LP) 

    if toggle_filtering:
      if toggle_stable_state:
        ctl.load(ss_filter_path)
      elif toggle_sync:
        ctl.load(sync_filter_path)
      elif toggle_async:
        ctl.load(async_filter_path)

  ctl.ground([("base", [])])
  functions = []

  with ctl.solve(yield_=True) as handle:
    for model in handle:
      functions.append(str(model).split(" "))
  
  global clingo_cumulative_level_search_time
  clingo_cumulative_level_search_time += float(ctl.statistics["summary"]["times"]["total"])
  
  return functions



#-----Main-----
if cmd_enabled:
  parseArgs()

printIFTVStart()
incst_LP, curated_LP = getInconsistenciesAndCuratedLP()

iftvs = generateInconsistentFunctionsAndTotalVars(incst_LP)
iftvs_LP, total_vars = processIFTVs(iftvs)
printIFTVEnd()

if iftvs_LP:
  for func in iftvs_LP.keys():

    printFuncRepairStart(func)

    original_LP = getOriginalModelLP(func)

    printNodeStart()
    nodes = generateNodes(iftvs_LP[func])
    nodes_LP = processNodes(nodes)
    printNodeEnd()

    if nodes_LP:

      if toggle_filtering:
        printNodeFilterStart()
        filtered_nodes = filterNodes(func, curated_LP, original_LP[0], nodes_LP)
        if filtered_nodes:
          nodes_LP = processFilteredNodes(filtered_nodes)
        else:
          print("No nodes respected the observations (FINISH SEARCH RIGHT HERE AT A LATER DATE; for now proceed with all nodes unfiltered for the sake of performance measuring)")
        printNodeFilterEnd()

      printEdgeStart()
      edges = generateEdges(nodes_LP)
      edges_LP = processEdges(edges)
      printEdgeEnd()

      if edges_LP:
        printFuncStart()
        node_levels = generateNodeLevels(iftvs_LP[func], nodes_LP)
        func_level = generateFuncLevel(iftvs_LP[func], original_LP[1])
        node_levels_LP = getNodeLevelsLP(node_levels)

        #LP containing LPs with variables, nodes, edges and node levels
        level_search_base_LP = combineLPs([iftvs_LP[func], nodes_LP, edges_LP, node_levels_LP])

        start_time = time.time()
        level_search_result = levelSearch(func, formatFuncLevel(func_level), total_vars[func], original_LP[0], curated_LP, level_search_base_LP)
        end_time = time.time()

        if level_search_result:
          functions = level_search_result[0]
          level = level_search_result[1]
          processFunctions(functions)

          printLevelSearchStatistics(end_time-start_time, clingo_cumulative_level_search_time, levels_searched, 
            formatFuncLevel(func_level), total_vars[func],level)
        else:
          printLevelSearchStatistics(end_time-start_time,clingo_cumulative_level_search_time,levels_searched,
            formatFuncLevel(func_level), total_vars[func])
        printFuncEnd()
        

    printFuncRepairEnd(func)
