#-----Level search auxiliary functions-----
#Inputs: A level, represented by an array of integers ordered in decreasing order
#Purpose: Find the index of the clause with the lowest number of missing variables
def findIdxOfLowestClause(level):
  for idx in range(len(level)-1, 0, -1): #travserse level in reverse order 
    if level[idx] < level[idx-1]:
      return idx
  
  return 0 #if all clauses have the same value, return the index of the first clause

#Input: Function level obtained from clingo
#Purpose: Function level formatted to array
def formatFuncLevel(func_level):
  func_level_formatted = []

  for clause in func_level[0]:
    arguments = clause.split(')')[0].split('(')[1].split(',')
    clause_level = arguments[1]
    func_level_formatted.append(int(clause_level))

  return sorted(func_level_formatted, reverse=True)



#-----Testing functions-----
#Inputs: Level to test
#Purpose: Used to test if level traversal is working as expected
def generateLevelCandidatesTest(level):
  candidates = []
  ''' 4 vars    
  candidates.append([0])
  candidates.append([1,1])
  candidates.append([1,1,1])
  candidates.append([1,1,1,1])
  candidates.append([2,1])
  candidates.append([2,1,1])
  candidates.append([2,2])
  candidates.append([2,2,1])
  candidates.append([2,2,2])
  candidates.append([2,2,2,2])
  candidates.append([2,2,2,2,2])
  candidates.append([2,2,2,2,2,2])
  candidates.append([3,1])
  candidates.append([3,2,2])
  candidates.append([3,2,2,2])
  candidates.append([3,3,2])
  candidates.append([3,3,3,3])
  '''


  '''3 vars'''
  candidates.append([0])
  candidates.append([1,1])
  candidates.append([1,1,1])
  candidates.append([2,1])
  candidates.append([2,2,2])
  


  if level in candidates:
    return True
  else:
    return False