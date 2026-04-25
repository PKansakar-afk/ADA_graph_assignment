# - Implements iterative DFS (using explicit stack) on roads.csv.
# - Records discovery time, finishing time, and parent of each vertex.
# - Classifies each edge as: tree, back, forward, or cross.
# - Prints a discussion of what the DFS reveals about the graph.

# Edge classification rules (for directed graphs):
#   Tree edge   : (u,v) where v was first discovered via u
#   Back edge   : (u,v) where v is an ancestor of u (still on stack / grey)
#   Forward edge: (u,v) where v is already fully finished AND disc[v] > disc[u]
#   Cross edge  : (u,v) where v is already fully finished AND disc[v] < disc[u]

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from graph_loader import load_directed_weighted

# DFS Implementation
class DFS:
    WHITE = 'WHITE'   # undiscovered
    GREY  = 'GREY'    # discovered, not yet finished
    BLACK = 'BLACK'   # fully finished

    def __init__(self, graph, nodes):
        self.graph  = graph
        self.nodes  = nodes

        self.color  = {n: self.WHITE for n in nodes}
        self.disc   = {}          # discovery time
        self.finish = {}          # finishing time
        self.parent = {n: None for n in nodes}
        self.edges  = []          # (u, v, classification)
        self.timer  = [0]         # mutable counter shared across calls

    def _dfs_visit(self, u):
        self.color[u]  = self.GREY
        self.timer[0] += 1
        self.disc[u]   = self.timer[0]

        for v, _ in self.graph[u]:
            if self.color[v] == self.WHITE:
                # Tree edge: v discovered for first time via u
                self.parent[v] = u
                self.edges.append((u, v, 'tree'))
                self._dfs_visit(v)

            elif self.color[v] == self.GREY:
                # Back edge: v is an ancestor (still on the call stack)
                self.edges.append((u, v, 'back'))

            elif self.color[v] == self.BLACK:
                # Forward or Cross — distinguish by discovery times
                if self.disc[u] < self.disc[v]:
                    self.edges.append((u, v, 'forward'))
                else:
                    self.edges.append((u, v, 'cross'))

        self.color[u]  = self.BLACK
        self.timer[0] += 1
        self.finish[u] = self.timer[0]

    def run(self):
        """Run full DFS (handles disconnected components)."""
        for n in self.nodes:
            if self.color[n] == self.WHITE:
                self._dfs_visit(n)
        return self

# Main
def run_b2(filepath):
    print("  B2 — DFS: Structure Analysis")
    print("-" * 55)

    graph, nodes, edges = load_directed_weighted(filepath)

    print(f"\nGraph edges:")
    for src, dst, w in edges:
        print(f"  {src} -> {dst}  (weight={w})")

    dfs = DFS(graph, nodes).run()

    # Vertex Table
    print(f"\n{'Vertex':<10} {'Disc':<8} {'Finish':<10} {'Parent'}")
    print("-" * 38)
    for n in nodes:
        p = dfs.parent[n] if dfs.parent[n] else "None (root)"
        print(f"  {n:<8} {dfs.disc[n]:<8} {dfs.finish[n]:<10} {p}")

    # Edge Classification Table
    print(f"\n{'Edge':<15} {'Type'}")
    print("-" * 30)
    for u, v, etype in dfs.edges:
        print(f"  {u} -> {v:<10}  {etype}")

    # Discussion
    back_edges    = [(u,v) for u,v,t in dfs.edges if t == 'back']
    tree_edges    = [(u,v) for u,v,t in dfs.edges if t == 'tree']
    forward_edges = [(u,v) for u,v,t in dfs.edges if t == 'forward']
    cross_edges   = [(u,v) for u,v,t in dfs.edges if t == 'cross']

    print("\n DFS Discussion")
    print(f"Tree edges    : {tree_edges or 'None'}")
    print(f"Back edges    : {back_edges or 'None'}")
    print(f"Forward edges : {forward_edges or 'None'}")
    print(f"Cross edges   : {cross_edges or 'None'}")

    if back_edges:
        print(f"\n CYCLE DETECTED — back edge(s) found: {back_edges}")
        print("A directed graph has a cycle if and only if DFS finds a back edge.")
    else:
        print("\n NO CYCLES — no back edges found.")
        print("This graph is a DAG (Directed Acyclic Graph).")

    print(f"\n Topological order hint (by decreasing finish time):")
    topo = sorted(nodes, key=lambda n: dfs.finish[n], reverse=True)
    print(f"{' -> '.join(topo)}")
    print("(Valid only if there are no back edges / cycles)\n")

    return dfs

if __name__ == '__main__':
    DATA_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'roads.csv')
    run_b2(DATA_PATH)