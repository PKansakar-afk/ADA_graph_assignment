# Utility to load roads.csv into an adjacency list representation. Used by all Part B algorithms.

import csv
from collections import defaultdict


def load_directed_weighted(filepath):
    """
    Loads a directed weighted graph from a CSV file.

    Returns:
        graph  : dict { node: [(neighbor, weight), ...] }
        nodes  : sorted list of all unique nodes
        edges  : list of (source, destination, weight)
    """
    graph = defaultdict(list)
    edges = []
    nodes = set()

    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            src = row['source']
            dst = row['destination']
            w   = int(row['weight'])
            graph[src].append((dst, w))
            edges.append((src, dst, w))
            nodes.add(src)
            nodes.add(dst)

    # Ensure every node appears in the graph dict even if it has no outgoing edges
    for n in nodes:
        if n not in graph:
            graph[n] = []

    return dict(graph), sorted(nodes), edges


def load_undirected_weighted(filepath):
    """
    Loads an undirected weighted graph from a CSV file.

    Returns:
        graph  : dict { node: [(neighbor, weight), ...] }
        nodes  : sorted list of all unique nodes
        edges  : list of (u, v, weight)
    """
    graph = defaultdict(list)
    edges = []
    nodes = set()

    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            u = row['u']
            v = row['v']
            w = int(row['weight'])
            graph[u].append((v, w))
            graph[v].append((u, w))
            edges.append((u, v, w))
            nodes.add(u)
            nodes.add(v)

    for n in nodes:
        if n not in graph:
            graph[n] = []

    return dict(graph), sorted(nodes), edges