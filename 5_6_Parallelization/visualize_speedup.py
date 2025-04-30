import matplotlib.pyplot as plt
import os

time = {1:1174.423, 2:665.374 , 4:391.46, 8:237.66, 16:149.9, 24:139.679}
# Extract number of processes and corresponding times
n_procs = list(time.keys())
times = list(time.values())

# Calculate speedup
base_time = times[0]
speedup = [base_time / t for t in times]

#Theoretical speedup
F = 0.92
theoretical_speedup = [1/(1-F+F/n) for n in n_procs]

# Plot theoretical speedup and actual speedup on the same plot
plt.figure(figsize=(10, 6))
plt.plot(n_procs, theoretical_speedup, marker='x', linestyle='--', color='r', label='Theoretical Speedup')
plt.plot(n_procs, speedup, marker='o', label='Actual Speedup')
plt.xlabel('Number of Processes')
plt.ylabel('Speedup')
plt.title('Speedup vs Number of Processes')
plt.legend()
plt.grid(True)
# Get the directory of the current script
current_dir = os.path.dirname(__file__)
# Ensure the 'plots' directory exists in the same folder as the script
plots_dir = os.path.join(current_dir, 'plots')
os.makedirs(plots_dir, exist_ok=True)
# Save the plot in the 'plots' folder in the same subfolder as the script
plt.savefig(os.path.join(plots_dir, 'point_5_speedup_dynamic_v2.png'))

print(
    f"Parallel fraction F = {F}, Serial Fraction B = 1 - F = {1-F}\n"
    f"Theoretical speedup S = 1/B = {1/(1-F)}\n"
    f"Speedup with 32 processors = {1/(1-F+F/24)}"
)