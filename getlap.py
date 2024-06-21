#!/usr/bin/env python
import os
import os.path
import sys
import math
from sys import argv
def getLines(file, critical_points):
  #Get line number of relevant eigenvalues
  cp, cp_lines = [], []
  for point in critical_points:
    new = "UniqueCP#:" + point
    cp.append(new)
  with open(file, 'r',) as CPFU00:
    e = 18
    for count, line in enumerate(CPFU00, 1):
      new_line = line.replace(' ','').strip()
      if new_line in cp:
        cp_lines.append(count + e)
  return cp_lines      
def getEigenvalues(file, line):
  #Return eigenvalues in int format
  with open(file, 'r') as CPFU00:
    eigenstring = CPFU00.readlines()[line - 1]
    eigenvalues = list(map(float,eigenstring.split()))
  return eigenvalues[0], eigenvalues[1], eigenvalues[2]
def getLap(x,y,z):
    laplacian = math.pow(x,2) + math.pow(y,2) + math.pow(z,2)
    return laplacian
def main():
    #Should eventually fix lap calculation in bader and make this obsolete
    from os.path import exists
    if not os.path.exists('CPFU00.dat'):
      print("There is no CPFU00.dat in the current directory!")
      return
    else:
      try:
        original_stdout = sys.stdout
        print("What we do not know is immense.")
        critical_points = argv[1:]
        cp_lines = getLines('CPFU00.dat',critical_points)
        critical_points = [eval(i) for i in critical_points]
        critical_points.sort()
        with open ('getlap.out', 'w') as getlap_out:
            sys.stdout = getlap_out
            for i, cp in enumerate(critical_points):
              print(f"Current CP is: {cp}")
              x , y , z = getEigenvalues('CPFU00.dat',cp_lines[i])
              print(f"Eigenvalues: {getEigenvalues('CPFU00.dat', cp_lines[i])}")
              print(f"Laplacian: {getLap(x, y ,z)}")
            sys.stdout = original_stdout
        getlap_out.close()
      except IndexError:
        print("Your Unique CP # does not match one listed in the CPFU00.dat or you repeated a CP #.")
        return
main()

