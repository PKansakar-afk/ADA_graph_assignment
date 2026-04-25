# B4: All-pairs shortest paths using Floyd-Warshall.

# - Builds a distance matrix for ALL pairs of nodes.
# - Detects negative cycles (diagonal becomes negative).
# - Reconstructs the path between any two nodes.
# - Compares Floyd-Warshall with repeated single-source Bellman-Ford.

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from graph_loader import load_directed_weighted

INF = float('inf')

# Floyd-Warshall Algorithm
def floyd_warshall(nodes, edges):
    # Floyd-Warshall all-pairs shortest path algorithm.

    # Time complexity : O(V^3)
    # Space complexity: O(V^2)

    # Args:
    #     nodes : list of all node names
    #     edges : list of (src, dst, weight)

    # Returns:
    #     dist  : 2D dict  dist[u][v]  = shortest distance u -> v
    #     next_ : 2D dict  next_[u][v] = next hop on path from u to v
    #     neg_cycle : bool — True if any negative cycle detected

    # Map node names to indices for clean matrix operations
    idx   = {n: i for i, n in enumerate(nodes)}
    V     = len(nodes)

    # Initialise distance matrix
    dist  = [[INF] * V for _ in range(V)]
    next_ = [[None] * V for _ in range(V)]

    # Zero diagonal
    for i in range(V):
        dist[i][i] = 0

    # Fill known edges
    for u, v, w in edges:
        i, j = idx[u], idx[v]
        if w < dist[i][j]: # keep smallest if parallel edges exist
            dist[i][j]  = w
            next_[i][j] = j

    # Core triple loop
    for k in range(V):
        for i in range(V):
            for j in range(V):
                if dist[i][k] != INF and dist[k][j] != INF:
                    new_dist = dist[i][k] + dist[k][j]
                    if new_dist < dist[i][j]:
                        dist[i][j]  = new_dist
                        next_[i][j] = next_[i][k]

    # Detect negative cycles: any node with negative self-distance
    neg_cycle = any(dist[i][i] < 0 for i in range(V))

    # Convert back to named dicts
    dist_named  = {u: {} for u in nodes}
    next_named  = {u: {} for u in nodes}
    for u in nodes:
        for v in nodes:
            i, j = idx[u], idx[v]
            dist_named[u][v]  = dist[i][j]
            nxt = next_[i][j]
            next_named[u][v]  = nodes[nxt] if nxt is not None else None

    return dist_named, next_named, neg_cycle

# Path Reconstruction
def reconstruct_path(next_, source, target):
    # Uses the 'next' matrix to reconstruct the path from source to target.
    # Returns list of nodes, or None if no path exists.

    if next_[source][target] is None:
        return None

    path = [source]
    node = source
    while node != target:
        node = next_[node][target]
        if node is None:
            return None
        path.append(node)
        if len(path) > len(next_) + 1: # cycle guard
            return None

    return path

# Print Helpers
def print_matrix(nodes, dist):
    # Pretty-prints the distance matrix.
    col_w = 12
    header = f"{'':>{col_w}}" + "".join(f"{n:>{col_w}}" for n in nodes)
    print("  " + header)
    print("  " + "-" * len(header))
    for u in nodes:
        row = f"{u:>{col_w}}"
        for v in nodes:
            d = dist[u][v]
            d_str = str(d) if d != INF else "∞"
            row += f"{d_str:>{col_w}}"
        print("  " + row)

# Main
def run_b4(filepath):
    print("=" * 60)
    print("  B4 — Floyd-Warshall: All-Pairs Shortest Paths")
    print("=" * 60)

    graph, nodes, edges = load_directed_weighted(filepath)

    print(f"\nGraph edges:")
    for src, dst, w in edges:
        print(f"  {src} -> {dst}  weight={w}")

    dist, next_, neg_cycle = floyd_warshall(nodes, edges)

    # Negative cycle check
    if neg_cycle:
        print("\nNEGATIVE CYCLE DETECTED in the graph.")
        print("All-pairs distances are not well-defined.")
    else:
        print("\nNo negative cycle detected.")

    # Distance matrix
    print(f"\nAll-Pairs Distance Matrix:")
    print()
    print_matrix(nodes, dist)

    # Path reconstructions
    print(f"\nPath Reconstructions (all reachable pairs):")
    print(f"{'Pair':<15} {'Distance':<12} {'Path'}")
    print("-" * 50)
    for u in nodes:
        for v in nodes:
            if u == v:
                continue
            d = dist[u][v]
            if d == INF:
                continue
            path = reconstruct_path(next_, u, v)
            path_str = " -> ".join(path) if path else "—"
            print(f"  {u+' -> '+v:<15} {str(d):<12} {path_str}")

    return dist, next_

if __name__ == '__main__':
    DATA_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'roads.csv')
    run_b4(DATA_PATH)