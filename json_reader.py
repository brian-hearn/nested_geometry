import json
import os

def main(n, d):
    # Construct the file path
    folder = f"nestedsolndata/d={d}"
    filename = f"nestedsolns_d={d}_n={n}.json"
    filepath = os.path.join(folder, filename)

    # Load JSON data
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return

    solutions = data.get("solutions", [])
    new_edges = data.get("new_edges", [])
    total_edges = data.get("total_edges", [])

    # Ensure all lists are the same length
    length = min(len(solutions), len(new_edges), len(total_edges))

    for i in range(length):
        print(f"Solution {i+1}: {solutions[i]}")
        print(f"  new_edges: {new_edges[i]}")
        print(f"  total_edges: {total_edges[i]}")
        print()


# n = input("Enter n: ")
# d = input("Enter d: ")
n = 110
d = 1
main(n, d)
