import argparse, logging, clingo
from math import comb
from aux_scripts.common import uniquify

#TODO - clean up & add cmd line support

#--Work in progress--
#Usage: $python repair.py
#Note: Model, observations and inconsistencies to be used by the algorithm have to be specified in the configs below


#-----Configs-----

#Toggle debug modes
iftv_debug_toggled = False
nodegen_debug_toggled = False
edgegen_debug_toggled = False
funcgen_debug_toggled = False


#Model path
model_path = "lp_models/corrupted/3/3-corrupted-f.lp"
#model_path = "lp_models/corrupted/8/8-corrupted-f.lp"
#model_path = "real_models/lp/corrupted/boolean_cell_cycle-corrupted-f.lp"


#Paths of expected observations
obsv_path = "lp_models/obsv/sstate/3-obs.lp"
#obsv_path = "lp_models/obsv/tseries/sync/3-obs.lp"
#obsv_path = "lp_models/obsv/tseries/async/3-obs.lp"

#obsv_path = "lp_models/obsv/sstate/8-obs.lp"
#obsv_path = "lp_models/obsv/tseries/sync/8-obs.lp"
#obsv_path = "lp_models/obsv/tseries/async/8-obs.lp"

#obsv_path = "real_models/lp/observations/tseries/sync/boolean_cell_cycle-obs.lp"
#obsv_path = "real_models/lp/observations/tseries/async/boolean_cell_cycle-obs.lp"


#Paths of encodings with inconsistencies
incst_path = "lp_models/corrupted/3/inconsistencies/3-corrupted-f-stable_inconsistency.lp"
#incst_path = "lp_models/corrupted/3/inconsistencies/3-corrupted-f-sync_inconsistency.lp"
#incst_path = "lp_models/corrupted/3/inconsistencies/3-corrupted-f-async_inconsistency.lp"

#incst_path = "./lp_models/corrupted/8/inconsistencies/8-corrupted-f-stable_inconsistency.lp"
#incst_path = "lp_models/corrupted/8/inconsistencies/8-corrupted-f-sync_inconsistency.lp"
#incst_path = "lp_models/corrupted/8/inconsistencies/8-corrupted-f-async_inconsistency.lp"

#incst_path = "lp_models/corrupted/boolean_cell_cycle/inconsistencies/boolean_cell_cycle-corrupted-f-sync_inconsistency.lp"


#Paths of encodings for obtaining inconsistent functions and total variables of each
iftv_path = "encodings/repairs/iftv.lp"

#Paths of encodings for generating nodes
nodegen_path = "encodings/repairs/node_generator.lp"

#Paths of encodings for generating edges between nodes
edgegen_path = "encodings/repairs/edge_generator.lp"

#Paths of encodings for generating functions
#funcgen_path = "encodings/repairs/func_generator.lp"
funcgen_path = "encodings/repairs/no_conversion/func_generator.lp"

#Paths of encodings for filtering generated functions
#ss_filter_path = "encodings/repairs/ss_func_filter.lp"
ss_filter_path = "encodings/repairs/no_conversion/ss_func_filter.lp"
#sync_filter_path = "encodings/repairs/sync_func_filter.lp"
sync_filter_path = "encodings/repairs/no_conversion/sync_func_filter.lp"
#async_filter_path = "encodings/repairs/async_func_filter.lp"
async_filter_path = "encodings/repairs/no_conversion/async_func_filter.lp"


#Mode flags 
toggle_stable_state = True
toggle_sync = False
toggle_async = False

#Global logger (change logging.(LEVEL) to desired (LEVEL) )
logging.basicConfig()
global_logger = logging.getLogger("global")
global_logger.setLevel(logging.DEBUG)



#-----Auxiliary Functions-----
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


#---Auxiliary clingo Functions---
class Context:
  #Input: n - objects; r - sample (both as clingo Symbols)
  #Purpose: used to efficiently calculate combinations (n choose r)
  def combination(n,r):
    N = clingo.Number
    combin = comb(n.number,r.number)
    return N(combin)



#-----Functions that create the LPs to be used by clingo-----
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

  for line in lines: 
    if f"function({func}" not in line and f"term({func}" not in line:
      original_LP += line
  return original_LP



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



#-----Functions that solve LPs with clingo-----
#Purpose: Obtains inconsistent functions, the variables and total number of variables of each function
def generateInconsistentFunctionsAndTotalVars():
  clingo_args = ["0"]
  if iftv_debug_toggled:
    clingo_args.append("--output-debug=text")

  ctl = clingo.Control(arguments=clingo_args, logger= lambda a,b: None)

  ctl.load(model_path)
  ctl.load(incst_path)
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
  ctl.load(incst_path)
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

#Input: The logic program containing information regarding the terms that can be used to create function candidates
#Purpose: Generates all possible function candidates with the given logic progam
def generateFunctions(original_LP,func,iftv_LP,nodes_LP,edges_LP):
  clingo_args = ["0", f"-c compound={func}"]
  if funcgen_debug_toggled:
    clingo_args.append("--output-debug=text")
    
  ctl = clingo.Control(arguments=clingo_args)

  ctl.add("base", [], program=original_LP)
  ctl.add("base", [], program=iftv_LP)
  ctl.add("base", [], program=nodes_LP)
  ctl.add("base", [], program=edges_LP)
  ctl.load(obsv_path)
  ctl.load(funcgen_path)

  if toggle_stable_state:
    ctl.load(ss_filter_path)
  elif toggle_sync:
    ctl.load(sync_filter_path)
  elif toggle_async:
    ctl.load(async_filter_path)

  print("Starting function generation \u23F1")
  ctl.ground([("base", [])], context=Context)
  functions = []

  with ctl.solve(yield_=True) as handle:
    for model in handle:
      functions.append(str(model).split(" "))
  
  print("Finished function generation \U0001F3C1")
  printStatistics(ctl.statistics)
  return functions



#-----Main-----
printIFTVStart()
iftvs = generateInconsistentFunctionsAndTotalVars()
processed_ifts_output = processIFTVs(iftvs)
printIFTVEnd()

if processed_ifts_output:
  for func in processed_ifts_output.keys():
    printFuncRepairStart(func)

    printNodeStart()
    nodes = generateNodes(processed_ifts_output[func])
    process_nodes_output = processNodes(nodes)
    printNodeEnd()

    if process_nodes_output:
      printEdgeStart()
      edges = generateEdges(process_nodes_output)
      process_edges_output = processEdges(edges)
      printEdgeEnd()

      if process_edges_output:
        printFuncStart()
        functions = generateFunctions(getOriginalModelLP(func),func,
          processed_ifts_output[func], process_nodes_output, process_edges_output)
        process_functions_output = processFunctions(functions)
        printFuncEnd()

    printFuncRepairEnd(func)

  
    