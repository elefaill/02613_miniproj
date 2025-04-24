import matplotlib.pyplot as plt
import os

time = {1:1205.15, 2:596.935 , 4:278.225, 8:231.496, 16:145.326, 24:139.336}
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
plt.savefig(os.path.join(plots_dir, 'point_5_speedup_dynamic_no_chunk.png'))

print(
    f"Parallel fraction F = {F}, Serial Fraction B = 1 - F = {1-F}\n"
    f"Theoretical speedup S = 1/B = {1/(1-F)}\n"
    f"Speedup with 32 processors = {1/(1-F+F/32)}"
)