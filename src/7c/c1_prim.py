# - Loads infra.csv (undirected weighted graph).
# - Implements Prim's algorithm using a min-heap.
# - Outputs total MST cost and the list of MST edges.
# - Discusses whether multiple MSTs exist.

# Prim's algorithm overview:
#   - Start from any arbitrary node.
#   - Greedily add the cheapest edge that connects a new (unvisited) node to the current growing tree.
#   - Repeat until all nodes are included.
#   - Uses a min-heap for efficient edge selection: O((V + E) log V)

import heapq
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from graph_loader import load_undirected_weighted

# Prim's Algorithm
def prim(graph, nodes, start=None):
    # Prim's MST algorithm using a min-heap.

    # Args:
    #     graph: dict { node: [(neighbor, weight), ...] }
    #     nodes: list of all node names
    #     start: starting node (defaults to first node if None)

    # Returns:
    #     mst_edges: list of (weight, u, v) edges in the MST
    #     total_cost: int/float total weight of the MST
    #     parent: dict { node: parent_node } in the MST tree

    if start is None:
        start = nodes[0]

    in_mst = set()
    parent = {n: None for n in nodes}
    key = {n: float('inf') for n in nodes}   # cheapest edge to reach n
    key[start] = 0

    # Min-heap entries: (edge_weight, node, parent_node)
    heap = [(0, start, None)]

    mst_edges  = []
    total_cost = 0

    while heap:
        cost, u, par = heapq.heappop(heap)

        if u in in_mst:
            continue

        in_mst.add(u)
        parent[u] = par

        if par is not None:
            mst_edges.append((cost, par, u))
            total_cost += cost

        # Explore u's neighbors
        for v, weight in graph[u]:
            if v not in in_mst and weight < key[v]:
                key[v] = weight
                heapq.heappush(heap, (weight, v, u))

    return mst_edges, total_cost, parent

# Multiple MST
def check_multiple_msts(edges, mst_edges):
    # Checks whether multiple MSTs might exist by looking for edges with duplicate weights that could be swapped.
    # An MST is unique if and only if no two edges in the graph share the same weight on any cut. If two edges crossing the same cut have equal weight, alternative MSTs may exist.

    mst_weights = sorted([w for w, _, _ in mst_edges])
    all_weights = sorted([w for _, _, w in edges])
    weight_counts = {}
    for w in all_weights:
        weight_counts[w] = weight_counts.get(w, 0) + 1

    duplicates = {w: c for w, c in weight_counts.items() if c > 1}
    return duplicates

# Main
def run_c1(filepath):
    print("C1 — Prim's Algorithm: Minimum Spanning Tree")
    print("-" * 60)

    graph, nodes, edges = load_undirected_weighted(filepath)

    print(f"\nGraph edges (undirected):")
    print(f"{'Edge':<15} {'Weight'}")
    print("-" * 25)
    for u, v, w in edges:
        print(f"{u+' -- '+v:<15} {w}")

    print(f"\nTotal nodes : {nodes}")
    print(f"Total edges : {len(edges)}")

    # Run Prim
    mst_edges, total_cost, parent = prim(graph, nodes, start='A')

    # MST Output
    print(f"\n{'-'*60}")
    print("MST RESULT")
    print(f"{'-'*60}")
    print(f"\nMST Edges (sorted by weight):")
    print(f"{'Edge':<15} {'Weight'}")
    print("-" * 25)
    for w, u, v in sorted(mst_edges):
        print(f"{u+' -- '+v:<15} {w}")

    print(f"\nTotal MST Cost: {total_cost}")
    print(f"Edges in MST: {len(mst_edges)}  (should be V-1 = {len(nodes)-1})")

    # MST Tree Structure
    print(f"\nMST Tree (parent pointers):")
    for node in nodes:
        p = parent[node] if parent[node] else "ROOT"
        print(f"{node}  <--  {p}")

    # Multiple MST Check
    print(f"\n{'-'*60}")
    print("MULTIPLE MSTs DISCUSSION")
    print(f"{'-'*60}")

    duplicates = check_multiple_msts(edges, mst_edges)

    if duplicates:
        print(f"""Duplicate edge weights found: {duplicates}""")
    else:
        print(f"""No duplicate edge weights found.""")

    return mst_edges, total_cost

if __name__ == '__main__':
    DATA_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'infra.csv')
    run_c1(DATA_PATH)