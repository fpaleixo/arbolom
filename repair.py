import argparse, logging, clingo
from math import comb
from aux_scripts.common import uniquify

#--Work in progress--
#Usage: $python repair.py
#Note: Model, observations and inconsistencies to be used by the algorithm have to be specified in the configs below

#TODO - comment things

#-----Configs-----

#Toggle debug mode
debug_toggled = False

#Model path
model_path = "lp_models/corrupted/3/3-corrupted-f.lp"

#Paths of expected observations
obsv_path = "lp_models/obsv/sstate/3-obs.lp"

#Paths of encodings with inconsistencies
incst_path = "./lp_models/corrupted/3/inconsistencies/3-corrupted-f-stable_inconsistency.lp"

#Paths of encodings for generating terms
termgen_path = "./encodings/repairs/term_generator.lp"

#Paths of encodings for generating functions
funcgen_path = "./encodings/repairs/func_generator.lp"

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

def termsMap(atoms):
  term_map = {}

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

  return term_map

def printTermsMap(term_map):
  print("Generated terms found \u2714\uFE0F  They are:")
  for func in term_map.keys():
    print("--Printing possible terms for function of " + func +"--")
    varnumber_map = term_map[func]
    for variable_number in dict(sorted(varnumber_map.items())).keys():
      print("Variables per term: " + variable_number)
      term_list = varnumber_map[variable_number]
      for term in term_list:
        if term != term_list[-1]:
          print(str(term),  end=" \033[1;32m | \033[0;37;40m")
        else:
          print(str(term))

def displayTerms(atoms):
  term_map = termsMap(atoms)
  printTermsMap(term_map)

#Inputs: atoms is a list with the atoms obtained from solving with clingo.
#Purpose: Prints clingo's solution in a more readable manner.
def printTerms(atoms):
  if not atoms:
    print("No answers sets could be found	\u2755 there must be something wrong with the encoding...")
  elif atoms[0]:
    displayTerms(atoms)
  else: 
    print("No atoms could be found \u274C")


#-----Auxiliary clingo Functions-----
class Context:
  #Input: n - objects; r - sample (both as clingo Symbols)
  #Purpose: used to efficiently calculate combinations (n choose r)
  def combination(n,r):
    N = clingo.Number
    combin = comb(n.number,r.number)
    return N(combin)

#-----Main-----
clingo_args = ["0"]
if(debug_toggled):
  clingo_args.append("--output-debug=text")
  
ctl = clingo.Control(arguments=clingo_args)

ctl.load(model_path)
ctl.load(obsv_path)
ctl.load(incst_path)
ctl.load(termgen_path)
ctl.load(funcgen_path)

ctl.ground([("base", [])], context=Context)
terms = []
with ctl.solve(yield_=True) as handle:
  for model in handle:
    terms.append(str(model).split(" "))

print(terms)
printTerms(terms)
printStatistics(ctl.statistics)
