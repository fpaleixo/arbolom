import argparse, logging, clingo
from math import comb
from aux_scripts.common import uniquify

#--Work in progress--
#Usage: $python repair.py
#Note: Model, observations and inconsistencies to be used by the algorithm have to be specified in the configs below

#-----Configs-----

#Toggle debug mode
debug_toggled = False

#Model path
model_path = "lp_models/corrupted/3/3-corrupted-f.lp"

#Paths of expected observations
obsv_path = "lp_models/obsv/sstate/3-obs.lp"

#Paths of encodings with inconsistencies
incst_path = "./lp_models/corrupted/3/inconsistencies/3-corrupted-f-stable_inconsistency.lp"

#Paths of encodings for repairs
repairs_path = "./encodings/repairs/all_candidates_stable.lp"

#Mode flags 
toggle_stable_state = True
toggle_sync = False
toggle_async = False

#Global logger (change logging.(LEVEL) to desired (LEVEL) )
logging.basicConfig()
global_logger = logging.getLogger("global")
global_logger.setLevel(logging.DEBUG)


#-----Auxiliary Functions-----
#Input: stats_dict dictionary from clingo.Control
#Purpose: Prints time statistics from clingo
def printStatistics(stats_dict):
  times = stats_dict["summary"]["times"]
  print("--Statistics--")
  print("Total: "+str(times["total"]) + "s (Solving: "+str(times["solve"])+"s)")
  print("CPU Time: "+str(times["cpu"])+"s")

#Inputs: term_map is the map created in displaySolution that will store term atoms.
#Purpose: Builds the term map by storing each term atom.
def buildTermMap(term_map, atom):
  arguments = atom.split(')')[0].split('(')[1].split(',')
  func = arguments[0]
  level = arguments[1]
  clause = arguments[3]
  variable = arguments[2]
  
  if func not in term_map.keys():
    term_map[func] = {}

  level_map = term_map[func]
  
  if level not in level_map.keys():
    level_map[level] = {}

  clause_map = level_map[level]

  if clause not in clause_map.keys():
    clause_map[clause] = [variable]
  else:
    clause_map[clause].append(variable)

#Inputs: func_map is the map created in displaySolution that will store function atoms.
#Purpose: Builds the function map by storing each function atom.
def buildFuncMap(func_map, atom):
  arguments = atom.split(')')[0].split('(')[1].split(',')
  func = arguments[0]
  id = arguments[1]
  clause_number = arguments[2]
  level = arguments[3]
  clause = arguments[4]

  if func not in func_map.keys():
    func_map[func] = {}

  clause_number_map = func_map[func]

  if clause_number not in clause_number_map.keys():
    clause_number_map[clause_number] = {}

  id_map = clause_number_map[clause_number]
  
  if id not in id_map.keys():
    id_map[id] = [(level,clause)]
  else:
    id_map[id].append((level,clause))

#Inputs: term_map is the map containing term atoms, and func_map containing the function atoms (both created in displaySolution).
#Purpose: Prints the contents of these maps.
def printMaps(term_map, func_map):
  if term_map:
      print("Generated terms found \u2714\uFE0F  They are:")
      for func in term_map.keys():
        print("--Printing possible terms for function of " + func +"--")
        level_map = term_map[func]
        for level in level_map.keys():
          print("Level " + level)
          clause_map = level_map[level]
          for clause in clause_map.keys():
            if clause != list(clause_map.keys())[-1]:
              print(clause + ":" + str(clause_map[clause]),  end=" \033[1;32m | \033[0;37;40m")
            else:
              print(clause + ":" + str(clause_map[clause]))

      if func_map:
        print("Function candidates found \u2B55  They are:")
        for func in func_map.keys():
          print("--Printing candidates for function of " + func +"--")
          clause_number_map = func_map[func]
          for clause_number in clause_number_map.keys():
            print("Clause number: " + clause_number)
            id_map = clause_number_map[clause_number]
            for id in id_map.keys():
              print(id + ":",  end=" ")
              levels_clauses = id_map[id]
              for lc in levels_clauses:
                current_level = lc[0]
                current_clause = lc[1]
                func_clause = term_map[func][current_level][current_clause]
                if lc != levels_clauses[-1]:
                  print(str(func_clause), end=" or ")
                else:
                  print(str(func_clause))
      else:
        print("--No function candidates found \u274C --")

#Inputs: atoms is the list of atoms given to printRepairs.
#Purpose: Organizes term and function atoms into maps and prints them to output (other atoms are simply printed with as they are).
def displaySolution(atoms):
  repairs = []
  term_map = {}
  func_map = {}

  for a in atoms:
    if "generated_term" in a:
      buildTermMap(term_map,a)
    elif "function_candidate" in a:
      buildFuncMap(func_map,a)
    else:
      repairs.append(a)

  printMaps(term_map, func_map)

  if repairs:
    print("Other atoms found \U0001f440  They are:")
    print(str(repairs))

#Inputs: atoms is a list with the atoms obtained from solving with clingo.
#Purpose: Prints clingo's solution in a more readable manner.
def printRepairs(atoms):
  if not atoms:
    print("No answers sets could be found	\u2755 there must be something wrong with the encoding...")
  elif atoms[0]:
    displaySolution(atoms)
  else: 
    print("No repairs could be found \u274C")


#-----Auxiliary clingo Functions-----
class Context:
  #Input: n - objects; r - sample (both as clingo Symbols)
  #Purpose: used to efficiently calculate combinations (n choose r)
  def combination(n,r):
    N = clingo.Number
    combin = comb(n.number,r.number)
    return N(combin)

#-----Main-----
clingo_args = []
if(debug_toggled):
  clingo_args = ["--output-debug=text"]
  
ctl = clingo.Control(arguments=clingo_args)

ctl.load(model_path)
ctl.load(obsv_path)
ctl.load(incst_path)
ctl.load(repairs_path)

ctl.ground([("base", [])], context=Context)
atoms = []
with ctl.solve(yield_=True) as handle:
  for model in handle:
    atoms = (str(model).split(" "))

#print(atoms)
printRepairs(atoms)
printStatistics(ctl.statistics)
