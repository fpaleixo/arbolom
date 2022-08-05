import clingo

ss_consistency_path = "./encodings/consistency/ss_consistency.lp"
sync_consistency_path = "./encodings/consistency/sync_consistency.lp"
async_consistency_path = "./encodings/consistency/async_consistency.lp"

def consistencyCheck(model, obsv, stable_flag, sync_flag, async_flag, path_mode=False):
  ctl = clingo.Control(arguments=["0"])

  if path_mode:
    ctl.load(model)
  else:
    ctl.add("base",[], program=model)

  ctl.load(obsv)

  if stable_flag:
    ctl.load(ss_consistency_path)
  elif sync_flag:
    ctl.load(sync_consistency_path)
  elif async_flag:
    ctl.load(async_consistency_path)
  else:
    print("No mode selected...")
    return None

  ctl.ground([("base", [])])
  atoms = []
  with ctl.solve(yield_=True) as handle:
    for model in handle:
      atoms = (str(model).split(" "))
  return atoms

#Inputs: atoms is a list of atoms obtained from solving with clingo.
#Purpose: Prints the obtained atoms in a more readable manner.
def isConsistent(atoms,stable_flag, sync_flag, async_flag, print_inconsistencies=False):
  if not atoms:
    print("No answers sets could be found	\u2755 \nPossible reasons for this include:\n"
      + "- Using the wrong update mode; \n- Defining a compound as an input compound"
      + " when its value changes over time in the observations (time-series only).")
  else:
    isConsistent = True
    inconsistent_LP = ""
    observations_LP = ""

    for atom in atoms:
      if "inconsistent" in atom:
        isConsistent = False
        inconsistent_LP += atom + ".\n"
      else:
        observations_LP += atom + ".\n"

    if not isConsistent:
      if print_inconsistencies:
        if stable_flag:
          print("Model is not consistent \u274C Inconsistent (experiment, compound, value): ")
        elif sync_flag:
          print("Model is not consistent \u274C Inconsistent (experiment, timestep, compound, value): ")
        elif async_flag:
          print("Model is not consistent \u274C Inconsistent (experiment, timestep, compound, value/other compound updated at the same time): ")  
        print(inconsistent_LP)
        
      return inconsistent_LP + "\n" + observations_LP
    
    else: 
      print("The model is consistent with the observations \u2714\uFE0F")
      return None