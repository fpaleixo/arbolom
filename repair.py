import argparse, logging, clingo
from aux_scripts.common import uniquify

#-----Configs-----

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
def printRepairs(atoms):
  if not atoms:
    print("No answers sets could be found	\u2755 there must be something wrong with the encoding...")
  elif atoms[0]:
    repairs = []
    func_map = {}
    print(atoms)
    for a in atoms:
      if "generated_term" in a:
        arguments = a.split(')')[0].split('(')[1].split(',')
        func = arguments[0]
        level = arguments[1]
        clause = arguments[3]
        variable = arguments[2]
        
        if func not in func_map.keys():
          func_map[func] = {}

        level_map = func_map[func]
        
        if level not in level_map.keys():
          level_map[level] = {}

        clause_map = level_map[level]

        if clause not in clause_map.keys():
          clause_map[clause] = [variable]
        else:
          clause_map[clause].append(variable)
      
      else:
        repairs.append(a)
    
    if func_map:
        print("Generated terms found \u2714\uFE0F  They are:")
        for func in func_map.keys():
          print("--Printing possible terms for function of " + func +"--")
          level_map = func_map[func]
          for level in level_map.keys():
            print("Level " + level)
            clause_map = level_map[level]
            for clause in clause_map.keys():
              print(clause + ":" + str(clause_map[clause]),  end=" | ")
            print()

    if repairs:
      print("Other atoms found \u2714\uFE0F  They are:")
      print(str(repairs))
  else: 
    print("No repairs could be found \u274C")



#-----Main-----
ctl = clingo.Control(arguments=[])

ctl.load(model_path)
ctl.load(obsv_path)
ctl.load(incst_path)
ctl.load(repairs_path)

ctl.ground([("base", [])])
atoms = []
with ctl.solve(yield_=True) as handle:
  for model in handle:
    atoms = (str(model).split(" "))

printRepairs(atoms)