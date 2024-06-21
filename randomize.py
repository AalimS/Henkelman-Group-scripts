#!/usr/bin/env python
import random
from ase import Atoms
from ase.io import read, write
import numpy as np
#randomizes atoms and overwrites POSCAR
def main():
    print("What's the most you ever lost on a coin toss?")
    struc = read('POSCAR', format = "vasp")
    atoms = struc.get_positions()
    new_positions = np.empty([len(atoms),3])
    for atom in range(0, len(atoms)):
        new_positions[atom] = atoms[atom] + random.random()
    struc.set_positions(new_positions)
    write("POSCAR", struc, format = "vasp")
main()
