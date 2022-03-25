import os, glob, clingo, re
from clingo.application import ApplicationOptions

#TODO - test correctness, support cmd line paths, get uniquify on the common.py

#-----Configs-----
generate_sync = False

observation_number = "2"
time_steps = "5"
models_to_obtain = "1"

model_path = "./lp_models/1.lp"

sync_path = "./encodings/sync_observations.lp"
async_path = "./encodings/async_observations.lp"

save_sync = "./lp_models/obsv/tseries/sync"
save_async = "./lp_models/obsv/tseries/async"


#-----Auxiliary Functions-----

#Input: Desired path
#Purpose: Returns given path if it doesn't exist yet, otherwise creates a
#new path with (1) or (2) or ... (n), depending on how many files have already been created with that path name 
def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + " (" + str(counter) + ")" + extension
        counter += 1

    return path


def on_model(m):
    print (m)


def saveObsToFile(atoms):
    experiments_observations = {}
    current_answer_set = 0

    answer_set_finished = False

    origin_path = None
    if generate_sync:
      origin_path = os.path.join(save_sync, os.path.basename(model_path).replace(".lp", "-obs.lp"))
    else:
      origin_path = os.path.join(save_async, os.path.basename(model_path).replace(".lp", "-obs.lp"))
    current_path = origin_path
    
    for atom in atoms:
        if "experiment" in atom:

            if answer_set_finished:
              current_answer_set += 1
              answer_set_finished = False
              

            exp_num = ''.join(d for d in atom if d.isdigit())

            if current_answer_set not in experiments_observations.keys():
              experiments_observations[current_answer_set] = {}
        
            experiments_observations[current_answer_set][exp_num] = [atom]
        
        elif "observation" in atom:

            answer_set_finished = True

            terms = re.search('\((.*)\)', atom).group(1)
            terms = terms.split(',')
            experiments_observations[current_answer_set][terms[0]] += [atom]

    for answer_set in range(0,current_answer_set+1):
      f = open(current_path, 'w')
      for item in experiments_observations[answer_set].items():
          sorted_atoms = sorted(item[1])
          for atom in sorted_atoms:
              f.write(atom+".\n")
          f.write("\n")
      f.close()
      current_path = uniquify(origin_path)


#-----Main-----

ctl = clingo.Control(arguments=["-c e=" + observation_number, "-c t=" + time_steps, " " + models_to_obtain])

ctl.load(model_path)

if generate_sync:
  ctl.load(sync_path)
else:
  ctl.load(async_path)

ctl.ground([("base", [])])
atoms = []
with ctl.solve(yield_=True) as handle:
        for model in handle:
            print(model)
            atoms += (str(model).split(" "))

print(atoms)
saveObsToFile(atoms)
