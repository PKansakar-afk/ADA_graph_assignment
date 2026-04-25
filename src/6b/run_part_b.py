import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from b1_bfs import run_b1
from b2_dfs import run_b2
from b3_dijkstra_bellman_ford import run_b3
from b4_floyd_warshall import run_b4

ROADS = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'roads.csv')

if __name__ == '__main__':

    print("\n" + "-" * 60)
    print("PART B — GRAPH ALGORITHMS")
    print("-" * 60 + "\n")

    # B1 — BFS
    run_b1(ROADS, source='A')

    print("\n" + "-" * 60 + "\n")

    # B2 — DFS
    run_b2(ROADS)

    print("\n" + "-" * 60 + "\n")

    # B3 — Dijkstra + Bellman-Ford
    run_b3(ROADS, source='A')

    print("\n" + "-" * 60 + "\n")

    # B4 — Floyd-Warshall
    run_b4(ROADS)

    print("\n" + "-" * 60)
    print("  PART B COMPLETE")
    print("-" * 60 + "\n")