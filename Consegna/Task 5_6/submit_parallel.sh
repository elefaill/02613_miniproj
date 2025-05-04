#!/bin/bash
#BSUB -J pi_splot
#BSUB -q hpc
#BSUB -W 2:00
#BSUB -n 24                     
#BSUB -R "rusage[mem=16GB]"     
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -R 'span[hosts=1]'      
#BSUB -o output/minip_dynamic_24_100_bdsl%J.out
#BSUB -e output/minip_dynamic_24_100_bds%J.err
#BSUB -B
#BSUB -N
#BSUB -u s243599@dtu.dk

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

for num_proc in 1 2 4 8 16 24; do
    echo "Running with $num_proc processes..."
    time python simulate_parallel_dynamic.py 100 $num_proc
done