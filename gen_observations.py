import os, argparse, logging, clingo, re
from aux_scripts.common import uniquify

#Usage: $python gen_observations.py -f (FILENAME) -async -e (NUMBER OF EXPERIMENTS) -t (TIME STEPS) -as (NUMBER OF ANSWER SETS)
#Optional flags:
#-async ->  Produces observations using the asynchronous mode.
#Variables:
#FILENAME ->  Path of file containing Boolean model in the BCF format written in lp.
#NUMBER OF EXPERIMENTS ->  The number of experiments (sets of observations) to generate.
#TIME STEPS ->  The number of time steps to consider in each experiment.
#NUMBER OF ANSWER SETS ->  The number of answer sets to obtain.

#Attention: Input file must be in the BCF format and follow the conventions of the .lp files in the lp_models folder (results will be unpredictable otherwise)

#-----Configs-----

#Command-line usage
cmd_enabled = True

#Model path
model_path = "./lp_models/1.lp"

#Sync/async flag 
generate_sync = True

#Generation settings
experiments_number = "2"
time_steps = "5"
models_to_obtain = "1"

#Encoding paths
sync_path = "./encodings/sync_observations.lp"
async_path = "./encodings/async_observations.lp"

#Save folder paths
save_sync = "./lp_models/obsv/tseries/sync"
save_async = "./lp_models/obsv/tseries/async"

#Parser (will only be used if command-line usage is enabled above)
parser = None
args = None
if(cmd_enabled):
  parser = argparse.ArgumentParser(description="Generate observations for a Boolean logical model in the BCF written in lp.")
  parser.add_argument("-f", "--model_to_observe", help="Path to model to generate observations for.")
  parser.add_argument("-async", "--asynchronous", action='store_true', help="Flag to generate asynchronous observations (default is synchronous).")
  parser.add_argument("-e", "--experiments_number", help="Number of experiments (sets of observations) to generate (default is " + experiments_number + ").")
  parser.add_argument("-t", "--time_steps", help="Number of time steps to consider in each experiment (default is " + time_steps + ").")
  parser.add_argument("-as", "--models_to_obtain", help="Number of answer sets to obtain (default is " + models_to_obtain + ").")
  args = parser.parse_args()

#Global logger (change logging.(LEVEL) to desired (LEVEL) )
logging.basicConfig()
global_logger = logging.getLogger("global")
global_logger.setLevel(logging.DEBUG)



#-----Auxiliary Functions-----

#Purpose: Parses the argument regarding which file to generate observations for.
def parseArgs():
  logger = logging.getLogger("parser")
  logger.setLevel(logging.DEBUG)

  global model_path, generate_sync, experiments_number, time_steps, models_to_obtain

  model_path = args.model_to_observe
  logger.debug("Obtained file: " + model_path)

  asynch = args.asynchronous
  experiments = args.experiments_number
  time = args.time_steps
  models = args.models_to_obtain

  if asynch:
    generate_sync = False
    logger.debug("Mode changed from synchronous to asynchronous.")
  
  if experiments:
    experiments_number = experiments
    logger.debug("Overriding experiment number:  " + experiments_number)

  if time:
    time_steps = time
    logger.debug("Overriding time steps:  " + time_steps)

  if models:
    models_to_obtain = models
    logger.debug("Overriding answer sets to obtain:  " + models_to_obtain)

  return


#Inputs: Obtained atoms from the solved model by clingo
#Purpose: Saves generated observations to file
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
if(cmd_enabled):
  parseArgs()

ctl = clingo.Control(arguments=["-c e=" + experiments_number, "-c t=" + time_steps, " " + models_to_obtain])

ctl.load(model_path)

if generate_sync:
  ctl.load(sync_path)
else:
  ctl.load(async_path)

ctl.ground([("base", [])])
atoms = []
with ctl.solve(yield_=True) as handle:
        for model in handle:
            atoms += (str(model).split(" "))

print("Clingo finished solving \u2714\uFE0F")
saveObsToFile(atoms)
