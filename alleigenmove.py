#!/usr/bin/env python
# atoms need to be moved in the direction of their eigenvectors or the opposite but follow
# opposite of reaction coordinate
# (atoms[pos] - cp[pos]) dot eigenvector > 0 means move with eigenvector
# and vice versa
import os.path
from ase import Atoms
from ase.io import read, write
import numpy as np
import itertools
def getEigLines(file,chosen_atoms):
  #Get line number of eigenvectors and eigenvalues
  with open(file, 'r') as CPFU00:
    CPFU = CPFU00.readlines()
    CPFU_new = []
    for line in CPFU:
        new_line = line.replace(" ","").strip()
        CPFU_new.append(new_line)
    CPFU00.close()
    for i in range(len(CPFU_new)):
        if CPFU_new[i] == str(chosen_atoms):
            eigval_line = i - 6
            eigvec_lines = i -4
            cp_line = i - 20
            break
  return eigval_line, eigvec_lines, cp_line
def getEigenvectors(file,  eigvec_lines):
  #Return eigenvectors in float format
  eigenvector = []
  with open(file, 'r') as CPFU00:
    for line in itertools.islice(CPFU00,eigvec_lines,eigvec_lines + 3): 
        eigenvector.append(list(map(float,line.split())))
  return eigenvector    
def getEigenvalues(file, eigval_line):
  # return eigenvalues in float format
  eigenvalues = []
  with open(file, 'r') as CPFU00:
    for line in itertools.islice(CPFU00,eigval_line,eigval_line + 1): 
        eigenvalues.append(list(map(float,line.split())))
  return eigenvalues[0]    
def opposite(all_vecs):
  #matrix in opposite direction
  all_vecs = np.multiply(all_vecs,-1.0)
  return all_vecs
def getRelEigenvector(eigenvalues, eigenvectors):
  real_vec = []
  for i in range(len(eigenvalues)):
    if eigenvalues[i] > 0:
      real_vec.append(eigenvectors[0][i])            
      real_vec.append(eigenvectors[1][i])            
      real_vec.append(eigenvectors[2][i]) 
      break
  return real_vec     
def getCP_POS(file,cp_line):
  lines, cp_pos =[], []
  with open(file, 'r') as CPFU00:
    for line in itertools.islice(CPFU00,cp_line,cp_line + 1): 
        cp_pos.append(list(map(float,line.split())))
  return cp_pos   
def move_atoms(cp_pos, real_vec, opp_vec,scale, chosen_POSCAR, move_option):
    #move the input atoms together or apart 
    struc = read('POSCAR', format = "vasp")
    atoms = struc.get_positions()
    for atom in range(0, len(atoms)):
      if (atom + 1) in chosen_POSCAR:
        if move_option == 1:
          if np.dot(atoms[atom] - cp_pos, real_vec) < 0:
            atoms[atom] = atoms[atom] + np.multiply(opp_vec, scale)
          elif np.dot(atoms[atom] - cp_pos, real_vec) > 0:
            atoms[atom] = atoms[atom] + np.multiply(real_vec, scale)
        else:  
          if np.dot(atoms[atom] - cp_pos, real_vec) > 0:
            atoms[atom] = atoms[atom] + np.multiply(opp_vec, scale)
          elif np.dot(atoms[atom] - cp_pos, real_vec) < 0:
            atoms[atom] = atoms[atom] + np.multiply(real_vec, scale)
    struc.set_positions(atoms)
    write("POSCAR_moved", struc, format = "vasp")
    return  
def main():
    from os.path import exists
    if not os.path.exists('CPFU00.dat'):
      print("There is no CPFU00.dat in the current directory!")
      return
    else:
      FILE = 'CPFU00.dat'
      pairs = int(input("How many pairs of atoms will be moved? "))
      scale = float(input("How much would you like to scale the eigenvectors by? "))
      for i in range(pairs):
        chosen_atoms = input("Which atoms would you like to move? ")
        move_option = int(input("Enter 1 to move atoms away or Enter 2 to move atoms together. "))
        chosen = chosen_atoms.replace(" ","").strip()
        chosen_POSCAR = list(map(int,chosen_atoms.split()))
        eigval_line, eigvec_lines,cp_line = getEigLines(FILE,chosen)
        eigenvectors = getEigenvectors(FILE,eigvec_lines)
        eigenvalues = getEigenvalues(FILE, eigval_line)
        cp_pos = getCP_POS(FILE, cp_line)
        real_vec = getRelEigenvector(eigenvalues, eigenvectors)
        #convert array to numpy for ASE
        np.asarray(real_vec)
        np.asarray(cp_pos)
        #matrix in opposite direction
        opp_vec = opposite(real_vec)
        #the finale
        move_atoms(cp_pos,real_vec, opp_vec, scale, chosen_POSCAR, move_option)
        #file with the new atoms is POSCAR_moved
      print("It was summer, now it's autumn.")
main()
