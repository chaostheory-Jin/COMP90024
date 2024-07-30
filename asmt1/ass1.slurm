#!/bin/bash

#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --time=0-03:00:00
time srun -n 4 python3 ass1.py

