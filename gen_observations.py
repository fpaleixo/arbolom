import os, argparse, logging, clingo, re

#Usage: $python gen_observations.py -f (FILENAME) -async -e (NUMBER OF EXPERIMENTS) -t (TIME STEPS) -s (SAVE_DIRECTORY)

#Optional flags:
#-async ->  Produces observations using the asynchronous mode.
#-s -> Path of directory to save generated observations (default is lp_models/obsv/tseries/(a)sync/(name_of_file))

#Variables:
#FILENAME ->  Path of file containing Boolean model in the BCF format written in lp.
#NUMBER OF EXPERIMENTS ->  The number of experiments (sets of observations) to generate.
#TIME STEPS ->  The number of time steps to consider in each experiment.
#SAVE_DIRECTORY -> Path of directory to save generated observations to.

#Attention: 
# Input file must be in the BCF format and follow the conventions of the 
# .lp files in the lp_models folder (results will be unpredictable otherwise)


#-----Configs-----

#Command-line usage
cmd_enabled = True

#Model path
model_path = "lp_models/1.lp"

#Sync/async flag 
generate_sync = True

#Generation settings
experiments_number = "2"
time_steps = "5"

#Encoding paths
sync_path = "encodings/observations/sync_observations.lp"
async_path = "encodings/observations/async_observations.lp"

#Write folder paths
write_folder = "simple_models/lp/observations/tseries"

#Parser (will only be used if command-line usage is enabled above)
parser = None
args = None
if(cmd_enabled):
  parser = argparse.ArgumentParser(description=
    "Generate observations for a Boolean logical model in the BCF written in lp.")
  parser.add_argument("-f", "--model_to_observe", help=
    "Path to model to generate observations for.")
  parser.add_argument("-async", "--asynchronous", action='store_true', help=
    "Flag to generate asynchronous observations (default is synchronous).")
  parser.add_argument("-e", "--experiments_number", help=
    "Number of experiments (sets of observations) to generate (default is " + 
    experiments_number + ").")
  parser.add_argument("-t", "--time_steps", help=
    "Number of time steps to consider in each experiment (default is " + 
    time_steps + ").")
  parser.add_argument("-s", "--save_directory", help=
    "Path of directory to save generated observations to.")
  args = parser.parse_args()

#Global logger (change logging.(LEVEL) to desired (LEVEL) )
logging.basicConfig()
global_logger = logging.getLogger("global")
global_logger.setLevel(logging.INFO)



#-----Auxiliary Functions-----
#Purpose: Parses the argument regarding which file to generate observations for.
def parseArgs():
  logger = logging.getLogger("parser")
  logger.setLevel(logging.INFO)

  global model_path, write_folder, generate_sync
  global experiments_number, time_steps

  model_path = args.model_to_observe
  write_folder = os.path.dirname(model_path)
  logger.debug("Obtained file: " + model_path)

  asynch = args.asynchronous
  experiments = args.experiments_number
  time = args.time_steps

  if asynch:
    generate_sync = False
    logger.info("Mode used: Asynchronous \U0001f331")
  
  else: 
    logger.info("Default mode: Synchronous \U0001f550")

  if(args.save_directory):
    write_folder = args.save_directory
    logger.info("Custom write folder is: "+ write_folder)
  
  if experiments:
    experiments_number = experiments
    logger.debug("Overriding experiment number:  " + experiments_number)

  if time:
    time_steps = time
    logger.debug("Overriding time steps:  " + time_steps)

  return


#Inputs: Obtained atoms from the solved model by clingo.
#Purpose: Saves generated observations to file.
def saveObsToFile(atoms):
    logger = logging.getLogger("saveToFile")
    logger.setLevel(logging.INFO)

    experiments_observations = {}

    origin_path = None
    filename = os.path.basename(model_path).replace(".lp", "-sync-obs.lp")
    if not generate_sync:
      filename = os.path.basename(model_path).replace(".lp", "-async-obs.lp")
  
    origin_path = os.path.join(write_folder, filename)
    current_path = origin_path

    for atom in atoms:
        if "experiment" in atom:              
            exp_num = ''.join(d for d in atom if d.isdigit())
            experiments_observations[exp_num] = [atom]
        
        elif "observation" in atom:
            terms = re.search('\((.*)\)', atom).group(1)
            terms = terms.split(',')
            experiments_observations[terms[0]] += [atom]

    if not os.path.exists(os.path.dirname(current_path)):
      os.makedirs(os.path.dirname(current_path))
      logger.info("Created directory: " + os.path.dirname(current_path))

    f = open(current_path, 'w')
    for item in experiments_observations.items():
        sorted_atoms = sorted(item[1])
        for atom in sorted_atoms:
            f.write(atom+".\n")
        f.write("\n")
    f.close()
    logger.info("Saved to: " + current_path)



#-----Main-----
if(cmd_enabled):
  parseArgs()

ctl = clingo.Control(arguments=["0", "-c e=" + experiments_number, "-c t=" + 
  time_steps])

ctl.load(model_path)

if generate_sync:
  ctl.load(sync_path)
else:
  ctl.load(async_path)

ctl.ground([("base", [])])
atoms = []
with ctl.solve(yield_=True) as handle:
        for model in handle:
            atoms = (str(model).split(" "))

print("Clingo finished solving \u2714\uFE0F")
saveObsToFile(atoms)
