#!/usr/bin/env python
from ase import Atoms
from ase.io import read, write
import numpy as np
import sys
from sys import argv
import geteigvec
def import_eigvec():
    return geteigvec.main()
def get_data(data):
# unpacking 3d array into 2d
    unpacked = [j for i in data for j in i]    
    # grouping eigenvectors by atom number
    eigenvectors_by_atom = {}
    for atom, eigenvector in unpacked:
        if atom not in eigenvectors_by_atom:
            eigenvectors_by_atom[atom] = [eigenvector.copy()]
        else:
            eigenvectors_by_atom[atom].append(eigenvector.copy())
    return eigenvectors_by_atom
def projection(a,b):
#projection of vector a onto vector b
#    return np.multiply((np.dot(a, b)/ np.linalg.norm(b)**2), b)
    return np.multiply((np.dot(a,b) / 1),b)
#Copies CONTCAR to POSCAR along with some other shit
def main():
    CCAR, PCAR = argv[1], argv[2]
    c_struc = read(CCAR, format = "vasp")
    c_atoms = c_struc.get_positions()
    p_struc = read(PCAR, format = "vasp")
    p_atoms = p_struc.get_positions()
    data = import_eigvec()
    final_data = get_data(data)
    print("USING CROSS PRODUCT OF VASP PROJECTIONS FOR THIS TEST.")
    for atom in final_data:
      count = 1
      for eigvec in final_data.get(atom,[]):
#        print("NORM OF EIGVEC IS ONE", np.linalg.norm(eigvec)**2)
        print("ATOM NUMBER: ", atom)
        print("POSCAR POSITION : ", p_atoms[atom])
        print("CONTCAR POSITION : ", c_atoms[atom])
        vasp_move = np.subtract(c_atoms[atom],p_atoms[atom])
        print("VASP MOVE: ", vasp_move)
        print("EIGENVECTOR: ", eigvec)
        #projection of vasp movement vector onto eigenvector
        proj = projection(vasp_move, eigvec)
        print("PROJECTION OF VASP ONTO EIGENVECTOR: ", proj)
        if count == 1:
            a = proj
        else:
            b = proj
        #component of vasp vector perpendicular to eigenvector
        #PERP = VASP MOVE - PROJECTION
#        perp = np.subtract(vasp_move, proj)
#        print("PERPENDICULAR VECTOR OF EIGENVECTOR: ", perp)
#        print("DOT PRODUCT OF PERP AND EIG: ", np.dot(perp, eigvec))
#        c_atoms[atom] -= proj
#        if count == 1:
#          c_atoms[atom] = perp + p_atoms[atom]
#        else:
#          c_atoms[atom] += perp
#        print("NEW CONTCAR POSITIONS: ", c_atoms[atom])
#        c_struc.set_positions(c_atoms)
        count +=1
#      write(CCAR, c_struc, format = "vasp")
      print("FIRST PROJECTION: ", a)
      print("SECOND PROJECTION: ", b)
      cross = np.cross(a,b)
      print("CROSS PRODUCT OF VASP PROJECTIONS: ", cross)
      c_atoms[atom] = p_atoms[atom] + cross
      print("NEW CONTCAR POSITIONS: ", c_atoms[atom])
      c_struc.set_positions(c_atoms)
      write(CCAR, c_struc, format = "vasp")
main()
