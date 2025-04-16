#!/bin/bash
#BSUB -J pi_splot
#BSUB -q c02613
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -W 0:30
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -o minip_%J.out
#BSUB -e minip_%J.err
#BSUB -B
#BSUB -N
#BSUB -u s243157@dtu.dk

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

time python simulate_cuda.py 10
