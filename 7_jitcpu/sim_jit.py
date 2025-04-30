# this is the code from the text of the mini-project adding THE JACOBI JIT FUNCTION
from os.path import join
import sys
from numba import jit
from time import perf_counter as time
import numpy as np
import random


def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask


def jacobi(u, interior_mask, max_iter, atol=1e-6):
    u = np.copy(u)

    for i in range(max_iter):
        # Compute average of left, right, up and down neighbors, see eq. (1)
        u_new = 0.25 * (u[1:-1, :-2] + u[1:-1, 2:] + u[:-2, 1:-1] + u[2:, 1:-1])
        u_new_interior = u_new[interior_mask]
        delta = np.abs(u[1:-1, 1:-1][interior_mask] - u_new_interior).max()
        u[1:-1, 1:-1][interior_mask] = u_new_interior

        if delta < atol:
            break
    return u

@jit(nopython=True)
def jacobi_jit(u, interior_mask, max_iter, atol=1e-6):
    u = u.copy()
    u_new = u.copy()
    for it in range(max_iter):
        delta = 0.0
        for i in range(1, u.shape[0] - 1):
            for j in range(1, u.shape[1] - 1):
                if interior_mask[i - 1, j - 1]: 
                    val = 0.25 * (
                        u[i-1, j] + u[i+1, j] + u[i, j-1] + u[i, j+1]
                    )
                    delta = max(delta, abs(u[i, j] - val))
                    u_new[i, j] = val
        if delta < atol:
            break
        tmp = u
        u = u_new
        u_new = tmp
    return u


def summary_stats(u, interior_mask):
    u_interior = u[1:-1, 1:-1][interior_mask]
    mean_temp = u_interior.mean()
    std_temp = u_interior.std()
    pct_above_18 = np.sum(u_interior > 18) / u_interior.size * 100
    pct_below_15 = np.sum(u_interior < 15) / u_interior.size * 100
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
    # building_ids = building_ids[:N]
    building_ids = random.sample(building_ids, N)

    # Load floor plans
    all_u0 = np.empty((N, 514, 514))
    all_interior_mask = np.empty((N, 512, 512), dtype='bool')
    for i, bid in enumerate(building_ids):
        u0, interior_mask = load_data(LOAD_DIR, bid)
        all_u0[i] = u0
        all_interior_mask[i] = interior_mask

    # Run jacobi iterations for each floor plan
    MAX_ITER = 20_000
    ABS_TOL = 1e-4

    #before compile once the jit function
    all_u0_c = np.random.rand(2, 2)
    all_interior_mask_c = np.random.rand(2, 2)
    jacobi_jit(all_u0_c, all_interior_mask_c, MAX_ITER, ABS_TOL)


    all_u = np.empty_like(all_u0)


    start = time()
    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        u = jacobi(u0, interior_mask, MAX_ITER, ABS_TOL)
        all_u[i] = u
    print(f"Original: {time() - start:.2f}s")

    start = time()
    
    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        u = jacobi_jit(u0, interior_mask, MAX_ITER, ABS_TOL)
        all_u[i] = u
    
    print(f"JIT: {time() - start:.2f}s")

