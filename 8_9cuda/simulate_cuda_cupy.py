from os.path import join
import sys
import random
import time
from numba import cuda
import numpy as np
import cupy as cp

def load_data(load_dir, bid):
    SIZE = 512
    u = cp.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = cp.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = cp.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

# CUDA kernel for one Jacobi iteration
@cuda.jit
def jacobi_kernel(u, u_new, interior_mask):
    i, j = cuda.grid(2)
    if 1 <= i < u.shape[0] - 1 and 1 <= j < u.shape[1] - 1:
        if interior_mask[i - 1, j - 1]:  # adjust for padded boundaries
            u_new[i, j] = 0.25 * (
                u[i+1, j] + u[i-1, j] + u[i, j+1] + u[i, j-1]
            )

def jacobi_cuda(u0, interior_mask, max_iter):
    # Copy inputs and allocate output
    u = u0.copy()
    u_new = u0.copy()
  
    # Configure thread and block sizes
    threads_per_block = (16, 16)
    blocks_per_grid_x = (u.shape[0] + threads_per_block[0] - 1) // threads_per_block[0]
    blocks_per_grid_y = (u.shape[1] + threads_per_block[1] - 1) // threads_per_block[1]
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

    # Transfer CuPy arrays to Numba device arrays
    u_d = cuda.to_device(u)
    u_new_d = cuda.to_device(u_new)
    mask_d = cuda.to_device(interior_mask)

    
    # Run Jacobi iterations
    for _ in range(max_iter):
        jacobi_kernel[blocks_per_grid, threads_per_block](u_d, u_new_d, mask_d)
        u_d, u_new_d = u_new_d, u_d  # Swap buffers

    return u_d

def summary_stats(u, interior_mask):
    u_interior = u[1:-1, 1:-1][interior_mask]
    mean_temp = u_interior.mean()
    std_temp = u_interior.std()
    pct_above_18 = cp.sum(u_interior > 18) / u_interior.size * 100
    pct_below_15 = cp.sum(u_interior < 15) / u_interior.size * 100
    return {
        'mean_temp': mean_temp,
        'std_temp': std_temp,
        'pct_above_18': pct_above_18,
        'pct_below_15': pct_below_15,
    }

if __name__ == '__main__':
    # Load data
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'

    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()

    if len(sys.argv) < 2:
        N = 1
    else:
        N = int(sys.argv[1])

    building_ids = random.sample(building_ids, N)

    # Load floor plans
    all_u0 = cp.empty((N, 514, 514))
    all_interior_mask = cp.empty((N, 512, 512), dtype='bool')
    for i, bid in enumerate(building_ids):
        u0, interior_mask = load_data(LOAD_DIR, bid)
        all_u0[i] = u0
        all_interior_mask[i] = interior_mask

    # Run CUDA Jacobi
    MAX_ITER = 20_000

    all_u = cp.empty_like(all_u0)
    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        print(f"Running Jacobi on GPU for building {i+1}/{N}")
        u = jacobi_cuda(u0, interior_mask, MAX_ITER)
        all_u[i] = u

    # Print summary statistics in CSV format
    stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    print('building_id, ' + ', '.join(stat_keys))  # CSV header
    for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
        stats = summary_stats(u, interior_mask)
        print(f"{bid},", ", ".join(str(stats[k]) for k in stat_keys))