#!/bin/bash
#SBATCH --job-name=disambiguation
#SBATCH --output=%A_%a.out
#SBATCH --error=%A_%a.err
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=11
#SBATCH --time=20:00:00
#SBATCH --mem=400g

# load python and packages
module add python
#export PYTHONPATH=/nas/longleaf/home/bill10/Library/lib/python3/:$PYTHONPATH

# Run python script
python3 disambiguate.py 
#python3 postprocessing.py
