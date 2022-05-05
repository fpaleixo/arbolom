import argparse, logging, clingo
from math import comb
from aux_scripts.common import uniquify

#--Work in progress--
#Usage: $python repair.py
#Note: Model, observations and inconsistencies to be used by the algorithm have to be specified in the configs below


#-----Configs-----

#Toggle debug modes
iftv_debug_toggled = False
nodegen_debug_toggled = False
funcgen_debug_toggled = False
candcheck_debug_toggled = False
edgegen_debug_toggled = False

#Model path
model_path = "lp_models/corrupted/3/3-corrupted-f.lp"
#model_path = "lp_models/corrupted/8/8-corrupted-f.lp"

#Paths of expected observations
obsv_path = "lp_models/obsv/sstate/3-obs.lp"
#obsv_path = "lp_models/obsv/tseries/sync/3-obs.lp"
#obsv_path = "lp_models/obsv/tseries/async/3-obs.lp"

#obsv_path = "lp_models/obsv/sstate/8-obs.lp"
#obsv_path = "lp_models/obsv/tseries/sync/8-obs.lp"
#obsv_path = "lp_models/obsv/tseries/async/8-obs.lp"

#Paths of encodings with inconsistencies
incst_path = "lp_models/corrupted/3/inconsistencies/3-corrupted-f-stable_inconsistency.lp"
#incst_path = "lp_models/corrupted/3/inconsistencies/3-corrupted-f-sync_inconsistency.lp"
#incst_path = "lp_models/corrupted/3/inconsistencies/3-corrupted-f-async_inconsistency.lp"

#incst_path = "./lp_models/corrupted/8/inconsistencies/8-corrupted-f-stable_inconsistency.lp"
#incst_path = "lp_models/corrupted/8/inconsistencies/8-corrupted-f-sync_inconsistency.lp"
#incst_path = "lp_models/corrupted/8/inconsistencies/8-corrupted-f-async_inconsistency.lp"

#Paths of encodings for obtaining inconsistent functions and total variables of each
iftv_path = "./encodings/repairs/iftv.lp"

#Paths of encodings for generating nodes
nodegen_path = "./encodings/repairs/node_generator.lp"

#Paths of encodings for generating edges between nodes
edgegen_path = "./encodings/repairs/edge_generator.lp"

#Paths of encodings for generating functions
funcgen_path = "./encodings/repairs/func_generator.lp"

#Paths of encodings for checking consistency
ss_consis_path = "encodings/repairs/single_consistency/ss_single_consistency.lp"
sync_consis_path = "encodings/repairs/single_consistency/sync_single_consistency.lp"
async_consis_path = "encodings/repairs/single_consistency/async_single_consistency.lp"

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

#Input: Map with generated terms
#Purpose: Prints the map containing generated terms in a more readable manner
def printTermsMap(term_map):
  print("Generated terms found \u2714\uFE0F")
  for func in term_map.keys():
    print("--Printing possible terms for function of: " + func)
    varnumber_map = term_map[func]
    for variable_number in dict(sorted(varnumber_map.items())).keys():
      print("Variables per term: " + variable_number)
      term_list = varnumber_map[variable_number]
      for term in term_list:
        if term != term_list[-1]:
          print(str(term),  end=" \033[1;32m | \033[0;37;40m")
        else:
          print(str(term))

#Input: Map with generated terms, map with function candidates
#Purpose: Prints the map containing function candidates in a more readable manner
def printFuncsMap(term_map, func_map):
  print("Function candidates found \u2B55")
  for func in func_map.keys():
    print("Printing candidates for function of: " + func)
    clause_number_map = func_map[func]
    for clause_number in dict(sorted(clause_number_map.items())).keys():
      print("Term number: " + clause_number)
      candidate_list = clause_number_map[clause_number]
      for candidate in candidate_list:
        for level_and_clause in candidate:
          current_level = level_and_clause[0]
          current_clause_idx = int(level_and_clause[1])-1
          func_clause = term_map[func][current_level][current_clause_idx]
          if level_and_clause != candidate[-1]:
            print(str(func_clause), end=" or ")
          else:
            print(str(func_clause))

#Input: Map with candidates that respect observations
#Purpose: Prints the map containing viable candidates in a more reaadable manner
def printViableCandidatesMap(viable_candidates_map):
  print("Viable function candidates: ")
  for func in viable_candidates_map.keys():
    print("Printing viable candidates for function of: " + func)

    for cand in viable_candidates_map[func]:
      print(cand)
    
    print(f"Total viable candidates: {len(viable_candidates_map[func])}" )

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

#Purpose: Prints the initial candidate checking phase message
def printCandCheckStart():
  print("\n\033[1;32m ----CANDIDATE CHECKING START----\033[0;37;40m")

#Purpose: Prints the final candidate checking phase message
def printCandCheckEnd():
  print("\n\033[1;32m ----CANDIDATE CHECKING END----\033[0;37;40m")


#---Auxiliary clingo Functions---
class Context:
  #Input: n - number of variables;
  #Purpose: used to calculate the total number of possible nodes (n choose 1 + n choose 2 + ... n choose n = 2^n)
  def totalNodes(n):
    N = clingo.Number
    total = pow(2,n.number) - 1 #Minus one because we are not interested in n choose 0
    return N(total)



#-----Functions that organize generated atoms in maps-----
#Input: The generated terms output from clingo
#Purpose: Creates the map of generated terms from clingo's output;
# also creates a map with the total variables of each inconsistent function (to be used when generating the LP for candidate generation) 
def getTermsMapAndTotalVars(atoms):
  term_map = {}
  total_variables = {}

  for answer_set in atoms:
    term = []

    for a in answer_set:
      if "generated_term" in a:
        arguments = a.split(')')[0].split('(')[1].split(',')
        func = arguments[0]
        variable_number = arguments[1]
        variable = arguments[2]

        term.append(variable)
        
        if func not in term_map.keys():
          term_map[func] = {}

        varnumber_map = term_map[func]
        
        if variable_number not in varnumber_map.keys():
          varnumber_map[variable_number] = []

        if(a == answer_set[-1] and term):
          term_list = varnumber_map[variable_number]
          term_list.append(term)

      elif "total_variables" in a:
        arguments = a.split(')')[0].split('(')[1].split(',')
        func = arguments[0]
        total_varno = arguments[1]

        if func not in total_variables.keys():
          total_variables[func] = total_varno

  return term_map, total_variables

#Input: The function candidates output from clingo
#Purpose: Creates the map of function candidates from clingo's output
def getFuncsMap(atoms):
  func_map = {}

  for answer_set in atoms:
    func_candidate = []

    for a in answer_set:
      if "function_candidate" in a:
        arguments = a.split(')')[0].split('(')[1].split(',')
        func = arguments[0]
        clause_number = arguments[1]
        term_level = arguments[2]
        term_clause = arguments[3]

        func_candidate.append((term_level,term_clause))

        if func not in func_map.keys():
          func_map[func] = {}

        clause_number_map = func_map[func]

        if clause_number not in clause_number_map.keys():
          clause_number_map[clause_number] = []

        if(a == answer_set[-1] and func_candidate):
          func_list = clause_number_map[clause_number]
          func_list.append(func_candidate)
  return func_map

#Input: The maps containing terms and functions generated by clingo
#Purpose: Build a map with all the candidates for each inconsistent function (with the candidates written in LP)
def getCandidatesMap(term_map, func_map):
  candidate_map = {}

  for func in func_map.keys():
    candidate_map[func] = []
    candidate_LP_list = candidate_map[func]

    original_model_LP = getOriginalModelLP(func) 
    candidate_LP_list.append(original_model_LP)

    clause_number_map = func_map[func]
    candidate_LP = ""

    for clause_number in clause_number_map.keys():
      candidate_list = clause_number_map[clause_number]

      for candidate in candidate_list:
        candidate_LP += "function(" + func + "," + clause_number + ").\n"
        current_clause_number = 1

        for level_and_clause in candidate:
          current_level = level_and_clause[0]
          current_clause_idx = int(level_and_clause[1])-1
          func_clause = term_map[func][current_level][current_clause_idx]

          for term in func_clause:
            candidate_LP += "term(" + func + f",{current_clause_number}," + term + ").\n"
          current_clause_number += 1
                
        candidate_LP_list.append(candidate_LP)
        candidate_LP = ""
  
  return candidate_map

#Input: The maps containing terms and functions generated by clingo
#Purpose: Obtain the candidates that are consistent with the observations
def getViableCandidatesMap(term_map, func_map):
  candidate_map = getCandidatesMap(term_map, func_map)
  consistent_candidates = {}

  for func in candidate_map.keys():
    func_candidates = candidate_map[func]
    total_candidates = len(func_candidates)
    original_LP = func_candidates[0]
    consistent_candidates[func] = []

    print_times = True
    if total_candidates > 100:
      print("Too many candidates to print times...")
      print_times = False
    
    for candidate_idx in range(1,len(func_candidates)):
      current_candidate = func_candidates[candidate_idx]

      complete_LP = original_LP + current_candidate
      
      inconsistencies = consistencyCheck(complete_LP,print_times,func)

      if not inconsistencies[0]:
        consistent_candidates[func].append(current_candidate)

  return consistent_candidates



#-----Functions that create the LPs to be used by clingo-----
#Input: The nodes generated from clingo
#Purpose: Creates the logic program that will be used to establish relations between nodes
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
    result_LP += f"node_id({current_node_id}).\n"

    for variable in node:
      var_name = variable.split(')')[0].split('(')[1]
      result_LP += f"node_variable({current_node_id},{var_name}).\n"
    
    result_LP += "\n"
    current_node_id += 1

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
#Purpose: Processes clingo's iftv output by creating an LP with them, forming a tuple with an inconsistent function and the respective
#number of total variables
def processIFTVs(iftvs):
  if not iftvs:
    print("No answers sets could be found	\u2755 there must be something wrong with the encoding...")

  elif iftvs[0]:

    iftvs_LP = getIftvsLP(iftvs)

    total_iftvs = len(iftvs)
    if(total_iftvs < 100):
      print("<Resulting inconsistent functions and total variables>")
      print(str(iftvs_LP))
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
      print(nodes_LP)
    else:
      print("Too many nodes to print...!")
    print(f"Total nodes: {total_nodes}")

    return nodes_LP

  else: 
    print("No nodes could be found \u274C")

#Input: The function candidates output from clingo
#Purpose: Processes clingo's function candidates output by creating a map with it and printing it
def processFunctions(atoms,terms_map):
  if not atoms:
    print("No answers sets could be found	\u2755 there must be something wrong with the encoding...")

  elif atoms[0]:
    func_output = getFuncsMap(atoms)

    size = len(atoms)
    if(size < 5000):
      printFuncsMap(terms_map,func_output)
    else:
      print("Too many candidates to print...")
    print("Total candidates: ",size)
    return func_output

  else: 
    print("No candidates could be found \u274C") 



#-----Functions that solve LPs with clingo-----
#Purpose: Generates all nodes containing the possible variable conjunctions
def generateInconsistentFunctionsAndTotalVars():
  clingo_args = ["0"]
  if iftv_debug_toggled:
    clingo_args.append("--output-debug=text")

  ctl = clingo.Control(arguments=clingo_args)

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
def generateFunctions(terms_LP):
  clingo_args = ["0"]
  if funcgen_debug_toggled:
    clingo_args.append("--output-debug=text")
    
  ctl = clingo.Control(arguments=clingo_args)

  ctl.add("base", [], program=terms_LP)
  ctl.load(funcgen_path)

  print("Starting function generation \u23F1")
  ctl.ground([("base", [])], context=Context)
  functions = []

  with ctl.solve(yield_=True) as handle:
    for model in handle:
      functions.append(str(model).split(" "))
  
  print("Finished function generation \U0001F3C1")
  printStatistics(ctl.statistics)
  return functions

#Input: The LP with the modified original model which now includes the new candidate
#Purpose: Use clingo to check if the given LP is consistent with the observations or not
def consistencyCheck(complete_LP, print_times,func):
  clingo_args = ["0", "-c compound="+func]
  if candcheck_debug_toggled:
    clingo_args.append("--output-debug=text")
    
  ctl = clingo.Control(arguments=clingo_args)

  ctl.add("base", [], program=complete_LP)
  ctl.load(obsv_path)

  if toggle_stable_state:
    ctl.load(ss_consis_path)
  elif toggle_sync:
    ctl.load(sync_consis_path)
  elif toggle_async:
    ctl.load(async_consis_path)

  if print_times:
    print("Starting candidate check \u23F1")

  ctl.ground([("base", [])], context=Context)
  inconsistencies = []

  with ctl.solve(yield_=True) as handle:
    for model in handle:
      inconsistencies += (str(model).split(" "))

  if print_times:
    print("Finished candidate check \U0001F3C1")
    printStatistics(ctl.statistics)

  return inconsistencies


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
      #TODO process_edges_output = processEdges(edges)
      print(edges)
      printEdgeEnd()

    printFuncRepairEnd(func)

"""   if process_terms_output:
    terms_map = process_terms_output[0]
    terms_LP = process_terms_output[1]
    #print(terms_LP)
    
    printFuncStart()
    functions = generateFunctions(terms_LP)
    process_func_output = processFunctions(functions,terms_map)
    printFuncEnd()

    if process_func_output:
      func_map = process_func_output

      printCandCheckStart()
      viable_candidates_map = getViableCandidatesMap(terms_map, func_map)
      printViableCandidatesMap(viable_candidates_map)
      printCandCheckEnd() """
  
    