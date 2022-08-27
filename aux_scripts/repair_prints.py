#Purpose: Prints the initial node generation phase message
def printFuncRepairStart(current_function):
  print(f"\033[1;32m ----{current_function} REPAIR START----\033[0;37;40m")

#Purpose: Prints the initial node generation phase message
def printFuncRepairEnd(current_function):
  print(f"\033[1;32m ----{current_function} REPAIR END----\033[0;37;40m")

#Purpose: Prints the initial iftv generation phase message
def printIFTVStart():
  print("\033[1;32m ----IFTV GENERATION START----\033[0;37;40m")

#Purpose: Prints the final iftv generation phase message
def printIFTVEnd():
  print("\033[1;32m ----IFTV GENERATION END----\033[0;37;40m")

#Inputs: The inconsistent function, and the resulting answer set obtained from clingo
#Purpose: Prints the repairs in LP format
def printRepairedLP(inconsistent_func, result):
  activators = ""
  inhibitors = ""

  node_max_ID = 1
  node_ID_map = {} 
  nodes = {}

  missing_regulator_no = 0
  extra_regulator_no = 0
  sign_change_no = 0
  node_number_change_no = 0
  missing_node_regulator_no = 0
  extra_node_regulator_no = 0

  if result =="timed_out":
    print("Timed out before determining consistent solutions...")

  elif result == "no_solution":
    print("No possible repairs found...")

  else:
    for atom in result:
      arguments = atom.split(')')[0].split('(')[1].split(',')

      if "regulator_activator" in atom:
        activators += f"regulates({arguments[0]}, {inconsistent_func}, 0).\n"
      
      elif "regulator_inhibitor" in atom:
        inhibitors += f"regulates({arguments[0]}, {inconsistent_func}, 1).\n"

      elif "node_regulator" in atom:
        unsorted_node_ID = arguments[0]
        regulator = arguments[1]

        #Makes sure nodes are outputted using ordered IDs
        if unsorted_node_ID not in node_ID_map.keys():
          node_ID_map[unsorted_node_ID] = node_max_ID
          node_max_ID += 1

        node_ID = node_ID_map[unsorted_node_ID]

        if node_ID in nodes:
          nodes[node_ID].append(regulator)
        else:
          nodes[node_ID] = [regulator]
      
      elif "missing_regulator" in atom:
        missing_regulator_no += 1

      elif "extra_regulator" in atom:
        extra_regulator_no += 1

      elif "sign_changed" in atom:
        sign_change_no += 1

      elif "node_number_changes" in atom:
        node_number_change_no = arguments[0]

      elif "missing_node_regulator" in atom:
        missing_node_regulator_no += 1
      
      elif "extra_node_regulator" in atom:
        extra_node_regulator_no += 1

    result = f"%Regulators of {inconsistent_func}\n" + activators + inhibitors +"\n"
    result += f"%Regulatory function of {inconsistent_func}\nfunction({inconsistent_func}, {len(nodes.keys())}).\n"

    for node_ID in nodes.keys():
      regulators = nodes[node_ID]

      for reg in regulators:
        result += f"term({inconsistent_func}, {node_ID}, {reg}).\n"
    
    print("\033[1;32mRepairs: \033[0;37;40m")

    print(result)

    printChanges(missing_regulator_no, extra_regulator_no, sign_change_no,
      node_number_change_no, missing_node_regulator_no, extra_node_regulator_no)

def printChanges(missing_regulator_no, extra_regulator_no, sign_change_no,
      node_number_change_no, missing_node_regulator_no, extra_node_regulator_no):
  print("\033[1;32mNumber of repairs of each type: \033[0;37;40m")
  print("Removed regulators - ", missing_regulator_no)
  print("Added regulators - ", extra_regulator_no)
  print("Changed regulator signs - ", sign_change_no)
  print("Node number variation (|original node number - final node number|) - ", node_number_change_no)
  print("Total regulators removed from nodes - ", missing_node_regulator_no)
  print("Total regulators added to nodes - ", extra_node_regulator_no)

#Inputs: The stats dictionary returned from clingo
def printStatistics(stats_dict):
  times = stats_dict["summary"]["times"]
  print("\n<Statistics>")
  print("Total: "+str(times["total"]) + "s (Solving: "+str(times["solve"])+"s)")
  print("CPU Time: "+str(times["cpu"])+"s")
  print("\n")