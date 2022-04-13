import argparse, logging, clingo
from aux_scripts.common import uniquify

#-----Configs-----

#Model path
model_path = "./lp_models/test.lp"

#Paths of encondings for repairs
ancestors_path = "./encodings/repairs/ancestors.lp"

#Mode flags 
toggle_stable_state = True
toggle_sync = False
toggle_async = False

#Global logger (change logging.(LEVEL) to desired (LEVEL) )
logging.basicConfig()
global_logger = logging.getLogger("global")
global_logger.setLevel(logging.DEBUG)



#-----Auxiliary Functions-----


def printAncestors(atoms):
  if not atoms:
    print("No answers sets could be found	\u2755 there must be something wrong with the encoding...")
  elif atoms[0]:
    print("Ancestors found \u2714\uFE0F  They are:")
    print(atoms)
  else: 
    print("No ancestors could be found \u274C")



#-----Main-----
ctl = clingo.Control()

ctl.load(model_path)
ctl.load(ancestors_path)

ctl.ground([("base", [])])
atoms = []
with ctl.solve(yield_=True) as handle:
  for model in handle:
    atoms += (str(model).split(" "))

printAncestors(atoms)