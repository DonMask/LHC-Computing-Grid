import matplotlib.pyplot as plt
import numpy as np

# Data from main.pdf (Section 3.1) + Scenario 2 (N=100, M=1000)
labels = ['Initial (N=50)', 'Optimized (N=50)', 'Scenario 2 (N=100)']
energy = [2907, 1854, 3700]  # kWh (Scenario 2 scaled from M=500 to M=1000)
time = [103.7, 100, 200]      # hours (Scenario 2 estimated)
gpu = [0, 50, 50]             # % (Scenario 2 similar GPU usage)
cost = [581.4, 370.8, 740]    # € (Scenario 2 scaled)

# Set up bar chart with dual Y-axis
x = np.arange(len(labels))
width = 0.2

fig, ax = plt.subplots(figsize=(10, 6))
ax2 = ax.twinx()  # Second Y-axis

# Plot bars
ax.bar(x - 1.5*width, energy, width, label='Energy (kWh)', color='#FF6384')
ax.bar(x - 0.5*width, cost, width, label='Cost (€)', color='#FF6F61')
ax2.bar(x + 0.5*width, time, width, label='Time (hours)', color='#32CD32')
ax2.bar(x + 1.5*width, gpu, width, label='GPU Tasks (%)', color='#1E90FF')

# Customize chart
ax.set_xlabel('Scenario')
ax.set_ylabel('Energy (kWh) / Cost (€)')
ax2.set_ylabel('Time (hours) / GPU Tasks (%)')
ax.set_title('Optimization HL-LHC Computing Grid: Energy, Time, GPU, Cost')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(loc='upper left')
ax2.legend(loc='upper right')

# Save chart
plt.tight_layout()
plt.savefig('optimization_chart_v2.png', dpi=300, bbox_inches='tight')
plt.close()
