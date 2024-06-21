#!/usr/bin/env python
import numpy as np
import ase
from ase import Atoms
from ase.io import read, write
from ase.io.vasp import read_vasp_xdatcar
from ase.io.trajectory import Trajectory
import matplotlib.pyplot as plt  # Import matplotlib
trajectory = ase.io.read('XDATCAR', index=":")
poscar = read('POSCAR', format='vasp')
p_atoms = poscar.positions
distances = []
for i, traj in enumerate(trajectory, 1):
#    print("FRAME: ", i)
#    print(traj.positions)
    if i == 1:
      distances.append(np.linalg.norm(traj.positions - p_atoms))
      previous_frame = traj.positions
      continue
    distances.append(np.linalg.norm(traj.positions - previous_frame))
    previous_frame = traj.positions
print(distances)
step_indices = list(range(1, len(distances) + 1))

# Plot the distances
plt.plot(step_indices, distances)
plt.xlabel('Step Index')
plt.ylabel('Distance')
plt.title('Distance vs. Step Index')
plt.grid(True)
plt.show()
