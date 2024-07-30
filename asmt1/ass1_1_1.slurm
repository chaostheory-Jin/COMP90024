#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=0-04:00:00
time srun -n 1 python3 ass1.py
