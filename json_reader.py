import json
import os

def load_data(n, d):
    folder = f"nestedsolndata/d={d}"
    filename = f"nestedsolns_d={d}_n={n}.json"
    filepath = os.path.join(folder, filename)

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None

    # Convert solutions -> list of lists of tuples
    raw_solutions = data.get("solutions", [])
    solutions = [[tuple(point) for point in sol] for sol in raw_solutions]

    new_edges = data.get("new_edges", [])
    total_edges = data.get("total_edges", [])

    return solutions, new_edges, total_edges

def print_output(data):
    solutions, new_edges, total_edges = data
    length = min(len(solutions), len(new_edges), len(total_edges))

    for i in range(length):
        # Convert tuples back to lists just for printing
        sol_as_lists = [list(pt) for pt in solutions[i]]

        print(f"Solution {i+1}: {sol_as_lists}")
        print(f"  new_edges: {new_edges[i]}")
        print(f"  total_edges: {total_edges[i]}")
        print()

# n = input("Enter n: ")
# d = input("Enter d: ")
n = 13
d = 1
data = load_data(n, d)
print_output(data)

print(data[0])
