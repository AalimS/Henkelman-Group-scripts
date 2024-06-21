#!/usr/bin/env python
from ase import Atoms
from ase.io import read, write
import numpy as np
import sys
from sys import argv
import re

def get_dimer_forces(OCAR, curvature):
  #This is disgusting but I don't know another way to do it
  with open(OCAR, "r") as outcar_file:
    text = outcar_file.read()
    lines = text.splitlines()
    force_text = 'Dimer: CN      ' + str(curvature)
    for line_number, line in enumerate(lines,1):
      if force_text in line:
        print(line_number)
        break
    global number_atoms
    start_line = int(line_number - 2 - (number_atoms/3))
    end_line = line_number - 2
    forces_lines = lines[start_line: end_line]
    forces_3d = [list(map(float, line.split())) for line in forces_lines]
    forces_3d_v1 = np.array(forces_3d)
    dimer_forces = forces_3d_v1.flatten()
  return dimer_forces
def get_CM_ANG(DCAR):
  curvature = None 
  angle = None
  with open(DCAR, "r") as dimcar_file:
    for line_number,line in enumerate(dimcar_file,0):
      columns = line.split()
      #Curvature is 5th column
      if line_number == 0:
        continue
      if float(columns[4]) < 0 and float(columns[5])< 1.0:
        curvature = float(columns[4])
        angle = float(columns[5])
        break
      elif columns[4] == '---':
        break
  return curvature, angle, line_number * 2
def main():
  PCAR, XDATCAR, DCAR, CCAR, scalar = argv[1], argv[2], argv[3], argv[4], int(argv[5])
  poscar, contcar, xdatcar= read(PCAR, format = "vasp"), read(CCAR, format="vasp"), read(XDATCAR, format="vasp-xdatcar")
  p_atoms, c_atoms = poscar.get_positions(), contcar.get_positions()
  global number_atoms
  number_atoms = len(p_atoms.flatten())
  curvature, angle, line_number = get_CM_ANG(DCAR) 
  print("FIRST NEGATIVE CURVATURE: ", curvature)
  print("FIRST ANGLE < 1.0: ", angle)
  if curvature < 0 and angle < 1.0:
      forces = get_dimer_forces(OCAR, curvature)
      print("FORCES len: ", len(forces))
      print("SCALING FORCES BY ", scalar)
      print("SCALED FORCES:") 
      print(np.multiply(scalar,forces))
      c_atoms_new = np.multiply(scalar, forces) + p_atoms.flatten()
      n = int(len(c_atoms_new) / 3)
      c_atoms_new = c_atoms_new.reshape(n , 3)
      contcar.set_positions(c_atoms_new)
      print("WRITING CALCULATED CONTCAR")
      write(CCAR, contcar, format="vasp") 
  else:
      print("NEGATIVE CURVATURE NOT FOUND OR ANGLE > 1.0")
      print("RUN ADDITIONAL DIMER STEPS")
main()
