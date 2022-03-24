import os, glob, clingo, re
from clingo.application import ApplicationOptions

#TODO - test correctness, do async encoding, support cmd line paths

#-----Configs-----

observation_number = "2"
time_steps = "3"
model_path = "./lp_models/1.lp"
ss_path = "./encodings/gen_observations.lp"

save_sync = "./lp_models/obsv/tseries/sync"



#-----Auxiliary Functions-----

def on_model(m):
    print (m)

def saveObsToFile(atoms):
    experiments_observations = {}

    current_path = os.path.join(save_sync, os.path.basename(model_path).replace(".lp", "-obs.lp"))
    f = open(current_path, 'w')
    
    for atom in atoms:
        if "experiment" in atom:
            exp_num = ''.join(d for d in atom if d.isdigit())
            experiments_observations[exp_num] = [atom]
        
        elif "observation" in atom:
            terms = re.search('\((.*)\)', atom).group(1)
            terms = terms.split(',')
            experiments_observations[terms[0]] += [atom]

    for item in experiments_observations.items():
        sorted_atoms = sorted(item[1])
        for atom in sorted_atoms:
            f.write(atom+".\n")
        f.write("\n")


#-----Main-----

ctl = clingo.Control(arguments=["-c e=" + observation_number, "-c t=" + time_steps])

ctl.load(model_path)
ctl.load(ss_path)
ctl.ground([("base", [])])

atoms = []
with ctl.solve(yield_=True) as handle:
        for model in handle:
            atoms += (str(model).split(" "))

saveObsToFile(atoms)
