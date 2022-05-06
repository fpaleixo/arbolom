import argparse, logging, clingo
from math import comb
from aux_scripts.common import uniquify

#!Deprecated
#!Deprecated
#!Deprecated

#Usage: $python overcomplex_repair.py
#Note: Model, observations and inconsistencies to be used by the algorithm have to be specified in the configs below

#-----Configs-----

#Toggle debug modes
termgen_debug_toggled = False
funcgen_debug_toggled = False
candcheck_debug_toggled = False

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


#Paths of encodings for generating terms
termgen_path = "./encodings/repairs/old_attempts/overcomplex/term_generator.lp"

#Paths of encodings for generating functions
funcgen_path = "./encodings/repairs/old_attempts/overcomplex/func_generator.lp"

#Paths of encodings for checking consistency
ss_consis_path = "encodings/repairs/old_attempts/overcomplex/single_consistency/ss_single_consistency.lp"
sync_consis_path = "encodings/repairs/old_attempts/overcomplex/single_consistency/sync_single_consistency.lp"
async_consis_path = "encodings/repairs/old_attempts/overcomplex/single_consistency/async_single_consistency.lp"

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

#Purpose: Prints the initial term generation phase message
def printTermStart():
  print("\033[1;32m ----TERM GENERATION START----\033[0;37;40m")

#Purpose: Prints the final term generation phase message
def printTermEnd():
  print("\n\033[1;32m ----TERM GENERATION END----\033[0;37;40m\n")

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
  #Input: n - objects; r - sample (both as clingo Symbols)
  #Purpose: used to efficiently calculate combinations (n choose r)
  def combination(n,r):
    N = clingo.Number
    combin = comb(n.number,r.number)
    return N(combin)



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
#Input: The output from getTermsMapAndTotalVars, containing the term map and number of total variables of each inconsistent function
#Purpose: Creates the logic program that will be used to generate function candidates
def getTermLP(term_output):
  term_map = term_output[0]
  total_vars = term_output[1]
  logic_program = ""

  for func in total_vars.keys():
    total = total_vars[func]
    logic_program += "total_variables(" + func + "," + total + ").\n"
  
  logic_program += "\n"

  for func in term_map.keys():
    varnumber_map = term_map[func]

    for variable_number in varnumber_map.keys():
      clause_id = 1
      term_list = varnumber_map[variable_number]

      for term in term_list:
        logic_program += "clause("+ func + "," + variable_number + f",{clause_id}).\n"

        for variable in term:
          logic_program += "generated_term("+ func + "," + variable_number + f",{clause_id}," + variable + ").\n"

        clause_id += 1
        logic_program += '\n'

  return logic_program

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
#Input: The generated terms output from clingo
#Purpose: Processes clingo's term generation output by creating a map with them, printing it, and using it to output the LP to be used 
# to generate function candidates
def processTerms(atoms):
  if not atoms:
    print("No answers sets could be found	\u2755 there must be something wrong with the encoding...")

  elif atoms[0]:
    term_output = getTermsMapAndTotalVars(atoms)

    size = len(atoms)
    if size < 5000:
      printTermsMap(term_output[0])
    else:
      print("Too many terms to print...")
    print("Total terms: ",size)

    logic_program = getTermLP(term_output)
    return term_output[0], logic_program

  else: 
    print("No terms could be found \u274C")

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
#Purpose: Generates all possible function terms that can be used to generate function candidates
def generateTerms():
  clingo_args = ["0"]
  if termgen_debug_toggled:
    clingo_args.append("--output-debug=text")

  ctl = clingo.Control(arguments=clingo_args)

  ctl.load(model_path)
  ctl.load(incst_path)
  ctl.load(termgen_path)

  print("Starting term generation \u23F1")
  ctl.ground([("base", [])])
  terms = []

  with ctl.solve(yield_=True) as handle:
    for model in handle:
      terms.append(str(model).split(" "))

  print("Finished term generation \U0001F3C1")
  printStatistics(ctl.statistics)
  return terms

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
printTermStart()
terms = generateTerms()
#print(terms)
process_terms_output = processTerms(terms)
printTermEnd()

if process_terms_output:
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
    printCandCheckEnd()

    