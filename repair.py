import argparse, logging, clingo, time
from aux_scripts.level_search import *
from aux_scripts.repair_prints import *

#--Work in progress--
#Usage: $python repair.py -f (FILENAME) -o (OBSERVATIONS) -i (INCONSISTENCIES) -stable -sync -async
#Optional flags:
#-stable -> Performs repairs using stable state observations (default).
#-sync -> Performs repairs using synchronous observations.
#-async -> Performs repairs using asynchronous observations.
#Variables:
#FILENAME -> Path of file containing Boolean model in the BCF format written in lp.
#OBSERVATIONS -> Path of file containing observations written in lp. 
#INCONSISTENCIES -> Path of file containing inconsistencies obtained from the consistency checking phase.


#-----Testing shortcuts (to be removed at a later date)----
'''
#3 variables
python .\repair.py -f simple_models/lp/corrupted/3/3-corrupted-f.lp -o simple_models/lp/observations/sstate/3-obs.lp -i simple_models/lp/corrupted/3/inconsistencies/3-corrupted-f-stable_inconsistency.lp -stable
python .\repair.py -f simple_models/lp/corrupted/3/3-corrupted-f.lp -o simple_models/lp/observations/tseries/sync/3-obs.lp -i simple_models/lp/corrupted/3/inconsistencies/3-corrupted-f-sync_inconsistency.lp -sync
python .\repair.py -f simple_models/lp/corrupted/3/3-corrupted-f.lp -o simple_models/lp/observations/tseries/async/3-obs.lp -i simple_models/lp/corrupted/3/inconsistencies/3-corrupted-f-async_inconsistency.lp -async

#5 variables
python .\repair.py -f simple_models/lp/corrupted/8/8-corrupted-f.lp -o simple_models/lp/observations/sstate/8-obs.lp -i simple_models/lp/corrupted/8/inconsistencies/8-corrupted-f-stable_inconsistency.lp -stable
python .\repair.py -f simple_models/lp/corrupted/8/8-corrupted-f.lp -o simple_models/lp/observations/tseries/sync/8-obs.lp -i simple_models/lp/corrupted/8/inconsistencies/8-corrupted-f-sync_inconsistency.lp -sync
python .\repair.py -f simple_models/lp/corrupted/8/8-corrupted-f.lp -o simple_models/lp/observations/tseries/async/8-obs.lp -i simple_models/lp/corrupted/8/inconsistencies/8-corrupted-f-async_inconsistency.lp -async

#6 variables
(no stable examples for boolean cell cycle)
python .\repair.py -f real_models/lp/corrupted/boolean_cell_cycle/boolean_cell_cycle-corrupted-f.lp -o real_models/lp/observations/tseries/sync/boolean_cell_cycle-obs.lp -i real_models/lp/corrupted/boolean_cell_cycle/inconsistencies/boolean_cell_cycle-corrupted-f-sync_inconsistency.lp -sync
python .\repair.py -f real_models/lp/corrupted/boolean_cell_cycle/boolean_cell_cycle-corrupted-f.lp -o real_models/lp/observations/tseries/async/boolean_cell_cycle-obs.lp -i real_models/lp/corrupted/boolean_cell_cycle/inconsistencies/boolean_cell_cycle-corrupted-f-async_inconsistency.lp -async

#7 variables
python .\repair.py -i simple_models/lp/corrupted/11/inconsistencies/11-corrupted-f2-stable_inconsistency.lp -o simple_models/lp/observations/sstate/11-obs.lp -f simple_models/lp/corrupted/11/11-corrupted-f2.lp -stable
python .\repair.py -f simple_models/lp/corrupted/11/11-corrupted-f.lp -o simple_models/lp/observations/tseries/sync/11-obs.lp -i simple_models/lp/corrupted/11/inconsistencies/11-corrupted-f-sync_inconsistency.lp -sync
python .\repair.py -f simple_models/lp/corrupted/11/11-corrupted-f.lp -o simple_models/lp/observations/tseries/async/11-obs.lp -i simple_models/lp/corrupted/11/inconsistencies/11-corrupted-f-async_inconsistency.lp -async

#8 variables
(no stable examples for sp1 cell)
python .\repair.py -f real_models/lp/corrupted/SP_1cell/SP_1cell-corrupted-f.lp -o real_models/lp/observations/tseries/sync/SP_1cell-obs.lp -i real_models/lp/corrupted/SP_1cell/inconsistencies/SP_1cell-corrupted-f-sync_inconsistency.lp -sync
(no async examples)

#All functions inconsistent
python .\repair.py -f simple_models/lp/corrupted/6/6-corrupted-fe.lp -o simple_models/lp/observations/sstate/6-obs.lp -i simple_models/lp/corrupted/6/inconsistencies/6-corrupted-fe-stable_inconsistency.lp -stable
python .\repair.py -f simple_models/lp/corrupted/6/6-corrupted-fe.lp -o simple_models/lp/observations/tseries/sync/6-obs.lp -i simple_models/lp/corrupted/6/inconsistencies/6-corrupted-fe-sync_inconsistency.lp -sync
python .\repair.py -f simple_models/lp/corrupted/6/6-corrupted-fe.lp -o simple_models/lp/observations/tseries/async/6-obs.lp -i simple_models/lp/corrupted/6/inconsistencies/6-corrupted-fe-async_inconsistency.lp -async

#NO SOLUTIONS
#5 variables
python .\repair.py -f simple_models/lp/corrupted/8/8-corrupted-f-nosol.lp -o simple_models/lp/observations/tseries/sync/8-obs.lp -i simple_models/lp/corrupted/8/inconsistencies/8-corrupted-f-nosol-sync_inconsistency.lp -sync

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
iftv_path = "encodings/repairs/iftv.lp"

#Paths of encodings for generating nodes
nodegen_path = "encodings/repairs/node_generator.lp"

#Paths of encodings for filtering generated nodes
ss_filternode_path = "encodings/repairs/filtering/node/ss_node_filter.lp"
sync_filternode_path = "encodings/repairs/filtering/node/sync_node_filter.lp"
async_filternode_path = "encodings/repairs/filtering/node/async_node_filter.lp"

#Paths of encodings for generating edges between nodes
edgegen_path = "encodings/repairs/edge_generator.lp"

#Paths of encodings for generating functions
ss_func_generator_path = "encodings/repairs/function_generators/func_generator_new_sstate.lp"
sync_func_generator_path = "encodings/repairs/function_generators/func_generator_new_sync.lp"
async_func_generator_path = "encodings/repairs/function_generators/func_generator_new_async.lp"


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


#Input: The base LP for function generation, the inconsistent function, the LP with the original model definition
#minus the inconsistent function, and the LP with the observations from the consistency checking phase
#Purpose: Uses clingo to generate functions based on observations
def generateFunctions(generate_functions_LP, func, original_LP, curated_LP):
  clingo_args = ["0", f"-c compound={func}"]
    
  ctl = clingo.Control(arguments=clingo_args)

  ctl.add("base", [], program=generate_functions_LP)
  ctl.add("base", [], program=original_LP)
  ctl.add("base", [], program=curated_LP) 

  if toggle_stable_state:
    ctl.load(ss_func_generator_path)
  elif toggle_sync:
    ctl.load(sync_func_generator_path)
  else:
    ctl.load(async_func_generator_path)
    
  ctl.ground([("base", [])])
  functions = []

  with ctl.solve(yield_=True) as handle:
    for model in handle:
      functions = str(model).split(" ")
  
  global clingo_cumulative_level_search_time
  clingo_cumulative_level_search_time += float(ctl.statistics["summary"]["times"]["total"])
  
  return functions



#-----Main-----
if cmd_enabled:
  parseArgs()

#TODO make this IFTV part clearer after edge flip and compound addition/removal is complete
#TODO Get inconsistent functions, variables and total variables 
printIFTVStart()
incst_LP, curated_LP = getInconsistenciesAndCuratedLP()

iftvs = generateInconsistentFunctionsAndTotalVars(incst_LP)
iftvs_LP, total_vars = processIFTVs(iftvs)
printIFTVEnd()

if iftvs_LP:
  for func in iftvs_LP.keys():

    printFuncRepairStart(func)

    original_LP = getOriginalModelLP(func)

    #Node generation
    printNodeStart()
    nodes = generateNodes(iftvs_LP[func])
    nodes_LP = processNodes(nodes)
    printNodeEnd()

    if nodes_LP:
      #Edge generation
      printEdgeStart()
      edges = generateEdges(nodes_LP)
      edges_LP = processEdges(edges)
      printEdgeEnd()

      if edges_LP:
        printFuncStart()

        #Function generation
        generate_functions_LP = combineLPs([iftvs_LP[func], nodes_LP, edges_LP])
        start_time = time.time()
        functions = generateFunctions(generate_functions_LP, func, original_LP[0], curated_LP)
        end_time = time.time()
        print(functions)

        printFunctionStatistics(end_time-start_time, clingo_cumulative_level_search_time, total_vars[func])
        printFuncEnd()
      
    printFuncRepairEnd(func)
