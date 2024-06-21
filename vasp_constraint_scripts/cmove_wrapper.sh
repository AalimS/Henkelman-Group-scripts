#!/bin/bash
#
#$ -cwd
#$ -N cross_5000
#$ -j y
#$ -V
#$ -pe mpi24 24
#$ -q all.q@@core24
#$ -o cmove_out
#$ -S /bin/bash

current_dir="/home/asa3674/c6h5cl/constraint_test/move_5000_cross"
#Needs to be a CPFU00.dat and geteigvec.in  in cwd
python /home/asa3674/geteigvec.py
for i in {1..5001}
do
  n=$((i-1))
  echo "-------------------------Submitting job for run $n...-------------------------"
  qsub "$current_dir/fri.sub"
  mpirun -n $NSLOTS /usr/local/bin/vasp_std
  cp CONTCAR CONTCAR_V
  echo "Processing run $n..."
  echo "CONTCAR path: $current_dir/CONTCAR"
  echo "POSCAR path: $current_dir/POSCAR"
  python /home/asa3674/cmove.py  "$current_dir/CONTCAR" "$current_dir/POSCAR"
  echo "Running vfin.pl for run $n..."
  vfin.pl "$current_dir/run$n"
  mv CONTCAR_V run$n
  echo "------------------------run $n complete---------------------------------------"
done

