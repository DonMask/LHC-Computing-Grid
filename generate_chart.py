import matplotlib.pyplot as plt
import numpy as np

# Data from main.pdf (Section 3.1)
labels = ['Initial', 'Optimized']
energy = [2907, 1854]  # kWh
time = [103.7, 100]     # hours
gpu = [0, 50]           # %
cost = [581.4, 370.8]   # €

# Set up bar chart
x = np.arange(len(labels))
width = 0.2

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - 1.5*width, energy, width, label='Energy (kWh)', color='#FF6384')
ax.bar(x - 0.5*width, time, width, label='Time (hours)', color='#FFCE56')
ax.bar(x + 0.5*width, gpu, width, label='GPU Tasks (%)', color='#9966FF')
ax.bar(x + 1.5*width, cost, width, label='Cost (€)', color='#FF6F61')

# Customize chart
ax.set_xlabel('Scenario')
ax.set_ylabel('Value')
ax.set_title('Optimization HL-LHC Computing Grid: Energy, Time, GPU, Cost')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

# Save chart
plt.tight_layout()
plt.savefig('optimization_chart.png', dpi=300, bbox_inches='tight')
plt.close()
