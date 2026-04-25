# B3: Dijkstra and Bellman-Ford comparison.

# - Dijkstra: single-source shortest path for NON-NEGATIVE weights.
#   Uses a min-heap (priority queue) for efficiency.

# - Bellman-Ford: single-source shortest path allowing NEGATIVE weights.
#   Relaxes all edges V-1 times and detects negative cycles.

# Both algorithms reconstruct shortest paths and are compared in output.

import heapq
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from graph_loader import load_directed_weighted

INF = float('inf')

# Dijkstra's Algorithm
def dijkstra(graph, nodes, source):
    # Dijkstra's single-source shortest path algorithm.
    # Correct ONLY when all edge weights are non-negative.

    # Uses a min-heap. Time complexity: O((V + E) log V)

    # Returns:
    #     dist   : dict { node: shortest_distance }
    #     parent : dict { node: parent_node }

    dist   = {n: INF for n in nodes}
    parent = {n: None for n in nodes}
    dist[source] = 0

    # Min-heap: (distance, node)
    heap = [(0, source)]

    visited = set()

    while heap:
        d, u = heapq.heappop(heap)

        # skip stale entry
        if u in visited:
            continue
        visited.add(u)

        for v, weight in graph[u]:
            if dist[u] + weight < dist[v]:
                dist[v]   = dist[u] + weight
                parent[v] = u
                heapq.heappush(heap, (dist[v], v))

    return dist, parent

# Bellman-Ford Algorithm
def bellman_ford(graph, nodes, edges, source):
    # Bellman-Ford single-source shortest path algorithm.
    # Handles negative edge weights.
    # Detects negative cycles.

    # Relaxes all |E| edges exactly |V|-1 times.
    # Time complexity: O(V * E)

    # Returns:
    #     dist            : dict { node: shortest_distance }
    #     parent          : dict { node: parent_node }
    #     negative_cycle  : bool — True if a negative cycle is reachable

    dist   = {n: INF for n in nodes}
    parent = {n: None for n in nodes}
    dist[source] = 0

    V = len(nodes)

    # Relax all edges V-1 times
    for iteration in range(V - 1):
        updated = False
        for u, v, weight in edges:
            if dist[u] != INF and dist[u] + weight < dist[v]:
                dist[v]   = dist[u] + weight
                parent[v] = u
                updated   = True
        if not updated:
            break # early termination means already converged

    # V-th pass: check for negative cycles
    negative_cycle = False
    for u, v, weight in edges:
        if dist[u] != INF and dist[u] + weight < dist[v]:
            negative_cycle = True
            break

    return dist, parent, negative_cycle


# Path Reconstruction (shared)
def reconstruct_path(parent, source, target):
    # Traces parent pointers from target back to source.
    if parent[target] is None and target != source:
        return None         # unreachable

    path = []
    node = target
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()

    if path[0] != source:
        return None
    return path


# Display Helper
def print_results(algo_name, dist, parent, nodes, source):
    print(f"\n[{algo_name}] Results from source '{source}':")
    print(f"{'Target':<10} {'Distance':<12} {'Path'}")
    print("-" * 45)
    for target in nodes:
        if target == source:
            continue
        d = dist[target]
        d_str = str(d) if d != INF else "UNREACHABLE"
        path = reconstruct_path(parent, source, target)
        path_str = " -> ".join(path) if path else "—"
        print(f"  {target:<10} {d_str:<12} {path_str}")


# Main
def run_b3(filepath, source='A'):
    print("B3 — Dijkstra vs Bellman-Ford Comparison")
    print("-" * 60)

    graph, nodes, edges = load_directed_weighted(filepath)

    print(f"\nGraph edges:")
    for src, dst, w in edges:
        print(f"  {src} -> {dst}  weight={w}")

    # Dijkstra
    print("\n DIJKSTRA (non-negative weights only)")
    print(f"{'─'*60}")

    has_negative = any(w < 0 for _, _, w in edges)
    if has_negative:
        print("Negative weights detected — Dijkstra skipped.")
        print("Dijkstra is only correct on non-negative weight graphs.")
    else:
        d_dist, d_parent = dijkstra(graph, nodes, source)
        print_results("Dijkstra", d_dist, d_parent, nodes, source)

    # Bellman-Ford
    print("\n BELLMAN-FORD (handles negative weights)")
    print(f"{'─'*60}")

    bf_dist, bf_parent, neg_cycle = bellman_ford(graph, nodes, edges, source)

    if neg_cycle:
        print("NEGATIVE CYCLE DETECTED — shortest paths are undefined.")
        print("Bellman-Ford identified that distances can decrease infinitely.")
    else:
        print("No negative cycle detected.")
        print_results("Bellman-Ford", bf_dist, bf_parent, nodes, source)

    # Side-by-side comparison
    if not has_negative and not neg_cycle:
        print("\n COMPARISON: Dijkstra vs Bellman-Ford")
        print(f"{'─'*60}")
        print(f"{'Target':<10} {'Dijkstra':<15} {'Bellman-Ford':<15} {'Match?'}")
        print("-" * 48)
        for t in nodes:
            if t == source:
                continue
            dd  = d_dist[t]
            bfd = bf_dist[t]
            match = "Yes" if dd == bfd else "No"
            dd_s  = str(dd)  if dd  != INF else "∞"
            bfd_s = str(bfd) if bfd != INF else "∞"
            print(f"  {t:<10} {dd_s:<15} {bfd_s:<15} {match}")
    return d_dist if not has_negative else None, bf_dist

if __name__ == '__main__':
    DATA_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'roads.csv')
    run_b3(DATA_PATH, source='A')