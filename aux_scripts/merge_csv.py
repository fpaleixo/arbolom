import os, argparse, glob, pandas as pd
#Usage: $python revision.py -f (FILENAME) -o (OBSERVATIONS) -stable -sync -async -bulk -benchmark (SAVE_PATH)
#Optional flags:
#-stable -> Performs repairs using stable state observations (default).
#-sync -> Performs repairs using synchronous observations.
#-async -> Performs repairs using asynchronous observations.
#-bulk -> Enables bulk revision (-f must be path of the directory with the models)
#-benchmark -> Enables benchmark mode
#Variables:
#FILENAME -> Path of file containing the BCF Boolean model written in .lp or .bnet format
#OBSERVATIONS -> Path of file containing observations written in lp. 
#SAVE_PATH -> Path of folder to save benchmark results to


csv_folder = "/content/drive/MyDrive/FCT/5o ano/2o semestre/arbolom_benchmarks/Results/boolean_cell_cycle/sync/Raw"
csv_name = os.path.basename(os.path.dirname(os.path.dirname(csv_folder)))

obsv_types = ["1-20", "1-3", "5-20", "5-3"]

#Parser
parser = None
args = None

#-----Auxiliary Functions-----
#---Argument parser---
#Purpose: Parses the arguments of function repair
def parseArgs():
  global parser, args

  parser = argparse.ArgumentParser(description="Merge the .csv files originated from benchmark.py (only works if used with the file structure of the benchmark files in the project page)")
  requiredNamed = parser.add_argument_group("required arguments")
  requiredNamed.add_argument("-f", "--csv_folder", help="Path of folder with the .csv files", required=True)
  args = parser.parse_args()

  global csv_folder

  csv_folder = args.csv_folder

#-----Main-----
parseArgs()
for o_type in obsv_types:
  files = [f for f in glob.glob(os.path.join(csv_folder, "*.csv")) if o_type in f]

  print(files)
  df = pd.concat(map(pd.read_csv, files), ignore_index=True)
  df.to_csv(os.path.join(os.path.dirname(csv_folder),"Merged", csv_name + "-" + o_type + "-" + os.path.basename(os.path.dirname(csv_folder)) + "-merged.csv"))
print("Done!")

