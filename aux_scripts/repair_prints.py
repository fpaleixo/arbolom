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

#Purpose: Prints the initial node generation phase message
def printNodeStart():
  print("\033[1;32m ----NODE GENERATION START----\033[0;37;40m")

#Purpose: Prints the final node generation phase message
def printNodeEnd():
  print("\n\033[1;32m ----NODE GENERATION END----\033[0;37;40m\n")

#Purpose: Prints the initial node filter phase message
def printNodeFilterStart():
  print("\033[1;32m ----NODE FILTER START----\033[0;37;40m")

#Purpose: Prints the final node filter phase message
def printNodeFilterEnd():
  print("\n\033[1;32m ----NODE FILTER END----\033[0;37;40m\n")

#Purpose: Prints the initial edge generation phase message
def printEdgeStart():
  print("\033[1;32m ----EDGE GENERATION START----\033[0;37;40m")

#Purpose: Prints the final edge generation phase message
def printEdgeEnd():
  print("\n\033[1;32m ----EDGE GENERATION END----\033[0;37;40m\n")

#Purpose: Prints the initial function generation phase message
def printFuncStart():
  print("\033[1;32m ----FUNCTION GENERATION START----\033[0;37;40m")

#Purpose: Prints the final function generation phase message
def printFuncEnd():
  print("\n\033[1;32m ----FUNCTION GENERATION END----\033[0;37;40m")