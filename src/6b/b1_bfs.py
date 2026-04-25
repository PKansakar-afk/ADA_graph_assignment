# B1: Unweighted reachability and hop distance using BFS.

# - Converts roads.csv into an UNWEIGHTED directed graph (ignoring edge weights).
# - From a source vertex s, computes minimum hops to all reachable nodes.
# - Reconstructs the path from s to any target t.

from collections import deque
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from graph_loader import load_directed_weighted

# BFS Implementation
def bfs(graph, source):
    # Performs BFS from `source` on an unweighted directed graph.

    # Args:
    #     graph  : dict { node: [(neighbor, weight), ...] }  — weights ignored
    #     source : starting node

    # Returns:
    #     dist   : dict { node: hop_count }   (unreachable nodes are absent)
    #     parent : dict { node: parent_node } (for path reconstruction)

    dist   = {source: 0}
    parent = {source: None}
    queue  = deque([source])

    while queue:
        current = queue.popleft()
        for neighbor, _ in graph[current]:          # weight is ignored
            if neighbor not in dist:                # not yet visited
                dist[neighbor]   = dist[current] + 1
                parent[neighbor] = current
                queue.append(neighbor)

    return dist, parent


def reconstruct_path(parent, source, target):
    # Traces back through parent pointers to rebuild the path from source to target.
    # Returns a list of nodes representing the path, or None if target is unreachable.

    # target was never reached
    if target not in parent:
        return None

    path = []
    node = target
    while node is not None:
        path.append(node)
        node = parent[node]

    path.reverse()

    # Path must start at source
    if path[0] != source:
        return None

    return path

# Main
def run_b1(filepath, source='A'):
    print("B1 — BFS: Unweighted Reachability and Hop Distance")
    print("-" * 55)

    graph, nodes, edges = load_directed_weighted(filepath)

    print(f"\nGraph edges (weights ignored for BFS):")
    for src, dst, w in edges:
        print(f"  {src} -> {dst}  (weight={w}, ignored)")

    print(f"\nRunning BFS from source: '{source}'\n")

    dist, parent = bfs(graph, source)

    print(f"{'Target':<10} {'Hops':<10} {'Path'}")
    print("-" * 40)
    for target in nodes:
        if target == source:
            continue
        if target in dist:
            path = reconstruct_path(parent, source, target)
            path_str = " -> ".join(path)
            print(f"  {target:<8} {dist[target]:<10} {path_str}")
        else:
            print(f"  {target:<8} {'UNREACHABLE':<10} —")

    print()
    return dist, parent


if __name__ == '__main__':
    DATA_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'roads.csv')
    run_b1(DATA_PATH, source='A')