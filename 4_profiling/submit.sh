#!/bin/bash
#BSUB -J pi_splot
#BSUB -q hpc
#BSUB -W 2:00
#BSUB -n 16                     
#BSUB -R "rusage[mem=16GB]"     
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -R 'span[hosts=1]'      
#BSUB -o minip_%J.out
#BSUB -e minip_%J.err
#BSUB -B
#BSUB -N
#BSUB -u s243157@dtu.dk

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

# 1. Run kernprof to collect line-profiling data
kernprof -l simulate.py 10

# 2. Analyze the collected data with line_profiler
python -m line_profiler simulate.py.lprof > simulate.txt
