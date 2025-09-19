import math
from itertools import combinations
from json_reader import *

def euclidean_distance(v1, v2):
    """Compute distance between two vectors (lists)."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

def count_close_pairs(vectors, d):
    """
    Counts the number of pairs of vectors in the list
    with distance <= d.
    """
    if d <= 0:
        raise ValueError("d must be positive")

    count = 0
    for v1, v2 in combinations(vectors, 2):
        if euclidean_distance(v1, v2) <= d:
            count += 1
    return count

# Returns all vectors within a distance d of (0,0)
def vectors_within_distance(dist):
    vectors = []
    for x in range(-math.ceil(dist), math.ceil(dist) + 1):
        for y in range(-math.ceil(dist), math.ceil(dist) + 1):
            if math.sqrt(x**2 + y**2) <= dist:
                vectors.append([x, y])
    return vectors

# Run
d = 3.2
dist = 11
vectors = vectors_within_distance(dist)
result = count_close_pairs(vectors, d)
print(f"Side of inputted solution: {len(vectors)}")
print(f"Join points within a distance of: {d}")
print(f"Number of pairs with distance <= {d}: {result}")
data = load_data(len(vectors), d)
optimal_nested_edges = data[2][0]
print(f"Edges in an optimal nested solution: {optimal_nested_edges}")

# Counterexamples:
# d = 2
# dist = 9.5
# Side of inputted solution: 293
# Join points within a distance of: 2
# Number of pairs with distance <= 2: 1590
# Edges in an optimal nested solution: 1587

# d = 2.25
# dist = 9.5
# Side of inputted solution: 293
# Join points within a distance of: 2.25
# Number of pairs with distance <= 2.25: 2590
# Edges in an optimal nested solution: 2580

# d = 2.85
# dist = 9.5
# Side of inputted solution: 293
# Join points within a distance of: 2.85
# Number of pairs with distance <= 2.85: 3068
# Edges in an optimal nested solution: 3067

# d = 3
# dist = 11
# Side of inputted solution: 377
# Join points within a distance of: 3
# Number of pairs with distance <= 3: 4632
# Edges in an optimal nested solution: 4624

# d = 3.2
# dist = 11
# Side of inputted solution: 377
# Join points within a distance of: 3.2
# Number of pairs with distance <= 3.2: 5864
# Edges in an optimal nested solution: 5854

# d = 4.15
# dist = 16
# Side of inputted solution: 797
# Join points within a distance of: 4.15
# Number of pairs with distance <= 4.15: 19738
# Edges in an optimal nested solution: 19726


