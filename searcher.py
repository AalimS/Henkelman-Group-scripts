#!/usr/bin/env python
from ase import Atoms
from ase.io import read, write
import numpy as np
import sys
from sys import argv
def get_neb_force(forces, parallel):
  #get NEB force
  #this is equal to the  force on the system  minus the force parallel to the band
  return forces - parallel
def get_parallel(forces, movement):
  # 2 * ( forces dot r) * r
  return 2 * (np.dot(forces, movement) * movement)   
def gradient_descent(magnitude, forces):    
  if magnitude > 0.01:
    forces_magnitude = np.linalg.norm(forces)
    scalar = 0.01 / forces_magnitude
    forces *= scalar
    print("SCALED FORCES")
    print(forces)
    print("NEW MAGNITUDE")
    print(np.linalg.norm(forces))
  if magnitude < 0.01:
    print("MAGNITUDE OF FORCES LESS THAN 0.01")
    print("STOPPING GRADIENT DESCENT")
    exit
  return forces
def delta_r(POSCAR, CONTCAR):
  #returns magnitude of positional difference between two images
  r = CONTCAR - POSCAR
  return np.linalg.norm(r)
def get_tangent(pre, mid, aft, improved_t):
  if improved_t == False:
    #improved_t false uses original tangent implementation
    #improve_t true bisects the two unit vectors
    print("USING NORMALIZED LINE SEGMENT")
    tangent = (aft - pre)/np.linalg.norm(aft - pre)
  else:
    print("USING BISECTED UNIT VECTORS")
    print("FIRST VECTOR NORMALIZED")
    v_1 = (mid - pre)/np.linalg.norm(mid - pre)
    print(v_1)
    print("SECONDS VECTOR NORMALIZED")
    v_2 =  (aft - mid)/np.linalg.norm(aft - mid)
    print(v_2)
    tangent = v_1 + v_2
  return tangent
def main():
  CCAR, PCAR, OCAR, PRECAR, AFTCAR, first_run = argv[1], argv[2], argv[3], argv[4], argv[5], int(argv[6])
  contcar, poscar, outcar = read(CCAR, format = "vasp"), read(PCAR, format = "vasp"), read(OCAR, format="vasp-out", index=0)
  c_atoms, p_atoms, out_forces = contcar.get_positions(), poscar.get_positions(), outcar.get_forces()

  #PRECAR is the image that goes back to ini and AFTCAR is the image that goes forward to fin. They also differ in their critical points.
  precar, aftcar, = read(PRECAR, format="vasp"), read(AFTCAR, format="vasp")
  pre_atoms, aft_atoms = precar.get_positions(), aftcar.get_positions()

  c_atoms_flat = c_atoms.flatten()
  p_atoms_flat = p_atoms.flatten()
  out_forces_flat = out_forces.flatten()
  aft_atoms_flat = aft_atoms.flatten()
  pre_atoms_flat = pre_atoms.flatten()
  print("PRECAR")
  print(pre_atoms_flat)
  print("AFTCAR")
  print(aft_atoms_flat)
  print("POSCAR")
  print(p_atoms_flat)
#  print("CONTCAR")
#  print(c_atoms_flat)

#  movement = c_atoms_flat - p_atoms_flat
#  print("R :(CONTCAR - POSCAR)")
#  print(movement)
  if first_run == 1:
    tangent = get_tangent(pre_atoms_flat, p_atoms_flat, aft_atoms_flat, False)
  else:
    tangent = get_tangent(pre_atoms_flat, p_atoms_flat, aft_atoms_flat, True)
  print("NORMALIZED TANGENT VECTOR")
  print(tangent)

  print("FORCES FROM OUTCAR")
   #Forces read from vasp outcar
  print(out_forces_flat)

#  print("MAGNITUDE OF MOVEMENT")
#  print(delta_r(c_atoms_flat,p_atoms_flat))

  print("FORCE & TANGENT DOT PRODUCT")
  print(np.dot(out_forces_flat, tangent))
  print("PARALLEL COMPONENT")
  #Parallel component of NEB force. 
  parallel = get_parallel(out_forces_flat, tangent)
  print(parallel)

  print("CALCULATED FORCE")
  #Full calculated NEB force
  calc_forces = get_neb_force(out_forces_flat, parallel)
  print(calc_forces)

  magnitude = np.linalg.norm(calc_forces)
  print("MAGNITUDE OF CALCULATED FORCE")
  print(magnitude)

  #Gradient descent performed on NEB force
  forces = gradient_descent(magnitude, calc_forces)
  #Reshaping CONTCAR array from flattened to array
  c_atoms_flat = p_atoms_flat + forces
  n = int(len(c_atoms_flat) / 3)
  c_atoms = c_atoms_flat.reshape(n , 3)

  print("DELTA R (CALC CONTCAR - POSCAR)")
  position_change = delta_r(c_atoms_flat,p_atoms_flat)
  print(position_change)
#  if position_change > 0.05:
#    print("DELTA R > 0.05\nSCALING CONTCAR")
#      scaling_factor = 0.05 / position_change
#    max_force = max(np.linalg.norm(forces))
#    scaling_factor = 0.05 / max_force
#    weights = np.linalg.norm(forces, axis=1) / max_force
#    c_atoms = p_atoms + (c_atoms - p_atoms) * scaling_factor * weights[:, np.newaxis]
#      c_atoms = p_atoms + (c_atoms - p_atoms) * scaling_factor  
#    print("NEW DELTA R")
#    print(delta_r(c_atoms,p_atoms)) 
  contcar.set_positions(c_atoms)
  print("WRITING CALCULATED CONTCAR")
  write(CCAR, contcar, format="vasp") 
main()
