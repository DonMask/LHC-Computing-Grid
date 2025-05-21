import numpy as np
import math
import random

# Parameters from the paper (Section 2.2, N=50, M=500)
N = 50  # Number of nodes
M = 500  # Number of tasks
T_max = 86400  # Maximum duration (1 day in seconds)
alpha = 0.6  # Weight for T_total
beta = 0.4  # Weight for E_total
cost_per_kwh = 0.2  # Energy cost (€/kWh)

# Node specifications (25 CPU + 25 GPU)
nodes = [
    {"type": "CPU", "c_i": 15e12, "P_TDP": 400, "f_i": 2.8, "f_max": 4.0, "M_i": 2e12, "B_i": 25e9}
    for _ in range(25)
] + [
    {"type": "GPU", "c_i": 30e12, "P_TDP": 800, "f_i": 4.0, "f_max": 4.0, "M_i": 2e12, "B_i": 25e9}
    for _ in range(25)
]

# Task specifications
tasks = [{"w_j": 280e9, "m_j": 128e9, "s_j": 2e6} for _ in range(M)]

# Energy parameters
PUE_uniform = 1.4
PUE_optimized = 1.2
E_trans = 0.08  # J/GB

# Simulated Annealing parameters
T_0 = 1000
T_min = 0.01
alpha_SA = 0.95
max_iter = 1000

def compute_task_metrics(node, task, PUE):
    """Compute the processing time and energy for a task on a given node."""
    w_j = task["w_j"]
    s_j = task["s_j"]
    c_i = node["c_i"]
    P_TDP = node["P_TDP"]
    f_i = node["f_i"]
    f_max = node["f_max"]

    # Processing time (t_j)
    t_j = (w_j * s_j) / c_i
    if node["type"] == "CPU":
        t_j *= (f_max / f_i)  # Adjust for CPU frequency

    # Adjusted power
    P_i = P_TDP * (f_i / f_max) ** 3

    # Processing energy
    e_ij = P_i * t_j * PUE

    # Transfer energy
    e_trans = E_trans * w_j

    return t_j, e_ij + e_trans

def check_constraints(allocation, nodes, tasks):
    """Verify if an allocation satisfies node constraints."""
    compute_load = [0] * N
    memory_load = [0] * N
    bandwidth_load = [0] * N

    for j, i in enumerate(allocation):
        if i is not None:
            w_j = tasks[j]["w_j"]
            s_j = tasks[j]["s_j"]
            m_j = tasks[j]["m_j"]
            compute_load[i] += w_j * s_j
            memory_load[i] += m_j
            bandwidth_load[i] += w_j

    for i in range(N):
        if compute_load[i] > nodes[i]["c_i"] * T_max:
            return False
        if memory_load[i] > nodes[i]["M_i"]:
            return False
        if bandwidth_load[i] > nodes[i]["B_i"] * T_max:
            return False

    return True

def compute_cost(allocation, nodes, tasks, PUE):
    """Compute total execution time and energy consumption."""
    T_total = 0
    E_total = 0
    gpu_tasks = 0

    node_times = [0] * N
    for j, i in enumerate(allocation):
        if i is not None:
            t_j, e_j = compute_task_metrics(nodes[i], tasks[j], PUE)
            node_times[i] += t_j
            E_total += e_j
            if nodes[i]["type"] == "GPU":
                gpu_tasks += 1

    T_total = max(node_times) if node_times else float("inf")
    cost = alpha * T_total + beta * (E_total / 3.6e6)  # Convert J to kWh
    return T_total, E_total, cost, gpu_tasks

def greedy_allocation(nodes, tasks):
    """Initial greedy allocation of tasks to nodes."""
    allocation = [None] * M
    available_c = [node["c_i"] * T_max for node in nodes]
    available_m = [node["M_i"] for node in nodes]
    available_b = [node["B_i"] * T_max for node in nodes]

    for j in range(M):
        best_i = None
        max_c = -1
        for i in range(N):
            if (tasks[j]["w_j"] * tasks[j]["s_j"] <= available_c[i] and
                tasks[j]["m_j"] <= available_m[i] and
                tasks[j]["w_j"] <= available_b[i] and
                nodes[i]["c_i"] > max_c):
                best_i = i
                max_c = nodes[i]["c_i"]

        if best_i is not None:
            allocation[j] = best_i
            available_c[best_i] -= tasks[j]["w_j"] * tasks[j]["s_j"]
            available_m[best_i] -= tasks[j]["m_j"]
            available_b[best_i] -= tasks[j]["w_j"]

    return allocation

def simulated_annealing(nodes, tasks, initial_allocation, PUE):
    """Optimize task allocation using Simulated Annealing."""
    allocation = initial_allocation.copy()
    _, _, current_cost, _ = compute_cost(allocation, nodes, tasks, PUE)
    best_allocation = allocation.copy()
    best_cost = current_cost

    T = T_0
    for iter in range(max_iter):
        # Generate neighbor: randomly move a task
        j = random.randint(0, M - 1)
        if allocation[j] is None:
            continue
        i_old = allocation[j]
        i_new = random.randint(0, N - 1)
        if i_new == i_old:
            continue

        new_allocation = allocation.copy()
        new_allocation[j] = i_new

        if check_constraints(new_allocation, nodes, tasks):
            _, _, new_cost, _ = compute_cost(new_allocation, nodes, tasks, PUE)
            delta_C = new_cost - current_cost

            if delta_C <= 0 or random.random() < math.exp(-delta_C / T):
                allocation = new_allocation
                current_cost = new_cost
                if new_cost < best_cost:
                    best_allocation = allocation.copy()
                    best_cost = new_cost

        T *= alpha_SA
        if T < T_min:
            break

    return best_allocation

def main():
    print("Simulating uniform allocation...")
    # Uniform allocation (all tasks to CPUs)
    uniform_allocation = [i % 25 for i in range(M)]  # Use only CPU nodes (0–24)
    T_total_uniform, E_total_uniform, _, gpu_tasks_uniform = compute_cost(
        uniform_allocation, nodes, tasks, PUE_uniform
    )
    cost_uniform = E_total_uniform / 3.6e6 * cost_per_kwh

    print(f"Uniform Allocation:")
    print(f"  T_total: {T_total_uniform:.0f} s ({T_total_uniform/3600:.1f} hours)")
    print(f"  E_total: {E_total_uniform/3.6e6:.0f} kWh")
    print(f"  Cost: {cost_uniform:.1f} €")
    print(f"  GPU tasks: {gpu_tasks_uniform/M*100:.0f}%")

    print("\nSimulating optimized allocation...")
    # Optimized allocation
    initial_allocation = greedy_allocation(nodes, tasks)
    optimized_allocation = simulated_annealing(nodes, tasks, initial_allocation, PUE_optimized)
    T_total_opt, E_total_opt, _, gpu_tasks_opt = compute_cost(
        optimized_allocation, nodes, tasks, PUE_optimized
    )
    cost_opt = E_total_opt / 3.6e6 * cost_per_kwh

    print(f"Optimized Allocation:")
    print(f"  T_total: {T_total_opt:.0f} s ({T_total_opt/3600:.1f} hours)")
    print(f"  E_total: {E_total_opt/3.6e6:.0f} kWh")
    print(f"  Cost: {cost_opt:.1f} €")
    print(f"  GPU tasks: {gpu_tasks_opt/M*100:.0f}%")

    # Savings
    energy_savings = (E_total_uniform - E_total_opt) / 3.6e6
    time_savings = (T_total_uniform - T_total_opt) / T_total_uniform * 100
    print(f"\nSavings:")
    print(f"  Energy: {energy_savings:.0f} kWh ({energy_savings/(E_total_uniform/3.6e6)*100:.0f}%)")
    print(f"  Time: {time_savings:.1f}%")
    print(f"  Cost: {(cost_uniform - cost_opt):.1f} €")

if __name__ == "__main__":
    main()
