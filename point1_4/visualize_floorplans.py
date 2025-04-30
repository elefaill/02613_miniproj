import numpy as np
import matplotlib.pyplot as plt
from os.path import join
import os

def load_building_data(load_dir, building_id):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))  # padded array
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{building_id}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{building_id}_interior.npy"))
    return u, interior_mask
 

 
def plot_building(u, interior_mask, building_id, output_dir="figures"):
    os.makedirs(output_dir, exist_ok=True)

    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    im0 = axs[0].imshow(u[1:-1, 1:-1], cmap='coolwarm', vmin=0, vmax=30)
    axs[0].set_title(f"Initial Temperature Grid\n(Building {building_id})")
    plt.colorbar(im0, ax=axs[0])

    im1 = axs[1].imshow(interior_mask, cmap='gray')
    axs[1].set_title(f"Interior Mask\n(Building {building_id})")
    plt.colorbar(im1, ax=axs[1])

    plt.tight_layout()
    save_path = os.path.join(output_dir, f"building_{building_id}.png")
    plt.savefig(save_path)
    print(f"Saved: {save_path}")
    plt.close()

LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
# You can also read the actual building_ids.txt if you want
example_building_ids = ['25806', '28082', '6086']  # Replace with real IDs available to you

for bid in example_building_ids:
    u, mask = load_building_data(LOAD_DIR, bid)
    plot_building(u, mask, bid)