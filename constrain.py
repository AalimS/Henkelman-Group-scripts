#!/usr/bin/env python
from ase.utils.geometry import sort 
from ase.io import read,write
import sys
from sys import argv
from ase.constraints import FixAtoms
#constrains or unconstrains atoms
#to use do ./constrain.py POSCAR 1 2 3 where 1 2 3 are indices of atoms to be constrained
#to unconstrain simply do ./constrain.py POSCAR
def main():
  poscar = argv[1]
  atoms = read(poscar,format = "vasp")
  if len(argv) == 2:
    atoms.set_constraint()
    write(poscar, atoms, format ="vasp")
    print("you are free...")
  else:
    indices_to_fix = [int(idx) for idx in sys.argv[2:]]
    # Ensure that indices are within the valid range
    valid_indices = [idx for idx in indices_to_fix if 0 <= idx < len(atoms)]
    if len(indices_to_fix) != len(valid_indices):
      print("Incorrect atom indices input. Try again!")
      return
    c = FixAtoms(indices=valid_indices)
    atoms.set_constraint(c)
    write(poscar, atoms, format="vasp")
    print("you are shackled...")
main()
