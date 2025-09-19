import matplotlib.pyplot as plt
import os
import math
import json
from json_reader import *

def distance(p, q):
    return math.hypot(p[0]-q[0], p[1]-q[1])

def f(s, x, y, d):
    """Count vectors in s within distance d of (x, y)"""
    return sum(1 for (a,b) in s if distance((a,b), (x,y)) <= d)

def normalize(solution):
    """Return canonical form of solution under translation/rotation/reflection"""
    points = solution
    def transforms(p):
        x,y = p
        return [
            ( x,  y), ( -x,  y), ( x, -y), (-x, -y),
            ( y,  x), ( -y,  x), ( y, -x), (-y, -x),
        ]
    all_variants = []
    for t_idx in range(8):
        transformed = [transforms(p)[t_idx] for p in points]
        minx = min(x for x,y in transformed)
        miny = min(y for x,y in transformed)
        shifted = sorted((x-minx, y-miny) for x,y in transformed)
        all_variants.append(tuple(shifted))
    return min(all_variants)

# ------------------------
# Save step PNG
# ------------------------
def save_step_png(solutions, step_idx, n, d, folder="nestedsolns"):
    if not solutions:
        return
    os.makedirs(os.path.join(folder, f"d={d}"), exist_ok=True)
    num_sols = len(solutions)
    cols = min(4, num_sols)
    rows = (num_sols + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(4*cols, 4*rows))
    if num_sols == 1:
        axes = [axes]
    else:
        axes = axes.flatten()

    for idx, sol in enumerate(solutions):
        xs, ys = zip(*sol)
        ax = axes[idx]
        ax.scatter(xs, ys, c="blue", s=100, zorder=2)
        for (x,y) in sol:
            ax.text(x+0.1, y+0.1, f"({x},{y})", fontsize=8)
        ax.set_aspect("equal")
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.set_xlim(min(xs)-1, max(xs)+1)
        ax.set_ylim(min(ys)-1, max(ys)+1)
        ax.set_title(f"Solution {idx+1}")

    for j in range(len(solutions), len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    filename = os.path.join(folder, f"d={d}", f"nestedsolns_d={d}_n={step_idx+1}.png")
    plt.savefig(filename)
    plt.close()
    print(f"Saved step {step_idx + 1} PNG with {len(solutions)} solutions: '{filename}'")

# ------------------------
# Save step info immediately after PNG
# ------------------------
def save_step_info(step_index, solutions, new_edges_list, total_edges_list, n, d, folder="nestedsolndata"):
    folder_path = os.path.join(folder, f"d={d}")
    os.makedirs(folder_path, exist_ok=True)
    serializable_solutions = [ [pt for pt in sol] for sol in solutions ]
    step_data = {
        'number_of_vertices': step_index + 1,
        'solutions': serializable_solutions,
        'new_edges': new_edges_list,
        'total_edges': total_edges_list
    }
    file_path = os.path.join(folder_path, f"nestedsolns_d={d}_n={step_index+1}.json")
    with open(file_path, "w") as f:
        json.dump(step_data, f, indent=4, default=str)
    print(f"Saved JSON to: '{file_path}'")

# ------------------------
# Main solver with step-by-step storage
# ------------------------
def generate_solutions_with_step_storage(n, d, init_solutions = [[(0,0)]], init_edges = 0, save_png=True):
    solutions = init_solutions
    chains = [[solution] for solution in init_solutions]
    init_num_vertices = len(init_solutions[0])
    if init_num_vertices == 1:
        # Step 0 info
        new_edges_list = [0]
        total_edges_list = [0]
        if save_png:
            save_step_png(solutions, 0, n, d)
        save_step_info(0, solutions, new_edges_list, total_edges_list, n, d)

    # Main loop
    for i in range(init_num_vertices+1, n+1):
        entries = []
        for sol, chain in zip(solutions, chains):
            min_x = min(p[0] for p in sol)
            max_x = max(p[0] for p in sol)
            min_y = min(p[1] for p in sol)
            max_y = max(p[1] for p in sol)
            candidates = [
                (x, y)
                for x in range(min_x-math.ceil(d), max_x+math.ceil(d)+1)
                for y in range(min_y-math.ceil(d), max_y+math.ceil(d)+1)
                if (x, y) not in sol
            ]
            for p in candidates:
                score = f(sol, p[0], p[1], d)
                entries.append((sol, chain, p, score))

        if not entries:
            solutions, chains = [], []
            break

        global_max = max(score for (_,_,_,score) in entries)

        seen = set()
        new_solutions = []
        new_chains = []
        new_edges_list = []
        total_edges_list = []

        for sol, chain, p, score in entries:
            if score != global_max:
                continue
            new_sol = sol + [p]
            key = normalize(new_sol)
            if key in seen:
                continue
            seen.add(key)
            new_solutions.append(new_sol)
            new_chains.append(chain + [new_sol])
            new_edges_list.append(score)
            # Compute cumulative total edges
            prev_total = sum(f(chain[j], *chain[j+1][-1], d) for j in range(len(chain)-1)) if len(chain) > 1 else 0
            prev_total += init_edges
            total_edges_list.append(prev_total + score)

        solutions = new_solutions
        chains = new_chains

        # Save PNG and step info
        if save_png:
            save_step_png(solutions, i-1, n, d)
        save_step_info(i-1, solutions, new_edges_list, total_edges_list, n, d)

    # Console output
    for idx, chain in enumerate(chains, 1):
        print(f"Chain {idx}:")
        total_edges = 0
        for step_idx, sol in enumerate(chain):
            if step_idx == 0:
                print(f"  Step {step_idx}: {sol}, new edges = 0, total edges = 0")
            else:
                new_point = sol[-1]
                prev = chain[step_idx-1]
                new_edges = f(prev, *new_point, d)
                total_edges += new_edges
                print(f"  Step {step_idx + 1}: add {new_point}, new edges = {new_edges}, total edges = {total_edges}")
        print()

    # Print total edges sequence for first chain
    if chains:
        chain = chains[0]
        total_edges = 0
        seq = [0]
        for i, sol in enumerate(chain):
            if i == 0:
                continue
            new_point = sol[-1]
            prev = chain[i-1]
            total_edges += f(prev, *new_point, d)
            seq.append(total_edges)
        print(f"Total edges sequence: {seq}")

    return chains

# Terminate after finding solutions with n vertices
n = 500
# Join all vertices within a distance of d with an edge
d = 2
# Toggle whether pngs of solutions are saved
save_png=True

# Specify initial solutions
# Can be loaded from existing JSONs

# Start from a single vertex
init_solutions = [[(0,0)]]
init_edges = 0

# Start from existing JSON data
# init_vertices = 250
# data = load_data(250, d)
# init_solutions = data[0]
# init_edges = data[2][0]

# Init grid for d = 5
# init_solutions = [[(i, j) for i in [0,-1,-2,-3] for j in [0,-1,-2,-3]]]

chains = generate_solutions_with_step_storage(n, d, init_solutions = init_solutions, init_edges = init_edges, save_png=save_png)

