#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --time=0-03:00:00
time srun -n 8 python3 ass1.py
