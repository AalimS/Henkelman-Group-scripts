#!/usr/bin/env python
import os.path
from ase import Atoms
from ase.io import read, write
import numpy as np
import itertools
import sys 
from sys import argv
def getEigLines(file,chosen_atoms):
  #Get line number of eigenvectors and eigenvalues
  chosen_atoms = str(chosen_atoms[1]) + str(chosen_atoms[2])
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
def atom_directions(cp_pos, real_vec, opp_vec, pair, move_option):
    #move the input atoms together or apart 
    struc = read('POSCAR', format = "vasp")
    atoms = struc.get_positions()
    data = []
    direction = 0
    for atom in range(0, len(atoms)):
      if (atom + 1) in pair[1:]:
        if move_option == 1:
          if np.dot(atoms[atom] - cp_pos, real_vec) < 0:
            direction = opp_vec
          elif np.dot(atoms[atom] - cp_pos, real_vec) > 0:
            direction = real_vec
        else:  
          if np.dot(atoms[atom] - cp_pos, real_vec) > 0:
            direction = opp_vec
          elif np.dot(atoms[atom] - cp_pos, real_vec) < 0:
            direction = real_vec
        data.append([atom, direction])
    return  data
def main():
    from os.path import exists
    if not os.path.exists('CPFU00.dat') or not os.path.exists('geteigvec.in'):
      print("There is no CPFU00.dat or geteigvec.in inside the current directory!")
      return
    else:
      FILE = 'CPFU00.dat'
      #structure of input file needs to be as follows
      #move_option  atom1    atom2
      #mov-option 1 moves atoms apart. option 2 moves atoms together
      #......
      INPUT = 'geteigvec.in'
      with open(INPUT, 'r') as IN:
        #read in geteigvec.in and convert string to list by line
        content = IN.readlines()
        lines = [line.strip() for line in content]
        new = [line.split() for line in lines]
        chosen = list(map(lambda x: list(map(int, x)), new))
      data = []
      for pair in chosen:
        #get eigenvector of positive eigenvalue and cp positions
        eigval_line, eigvec_lines,cp_line = getEigLines(FILE,pair)
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
        move_option = pair[0]
       # with open('geteigvec.out','a') as OUT:
        string = atom_directions(cp_pos,real_vec, opp_vec, pair, move_option)
        data.append(string)        
       #   OUT.write(str(string))
       #   OUT.write("\n")
    return data
main()
