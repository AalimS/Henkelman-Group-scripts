#!/usr/bin/env python
from ase.io import read,write
from ase import Atoms
import sys
from sys import argv
INPUT = argv[1]
struc = read(INPUT,format = "vasp")
cell = struc.cell
atoms = struc.get_positions()
struc.set_positions(atoms)
write(INPUT, struc, format = "vasp")
