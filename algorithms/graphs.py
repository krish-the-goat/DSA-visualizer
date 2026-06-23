"""
Graph traversal logic — BFS aur DFS.
Graph yahan ek adjacency list (dict) ke roop mein represent hota hai.
"""

import math


def build_graph_positions(graph):
    nodes = list(graph.keys())
    n = len(nodes)
    positions = {}

    for i, node in enumerate(nodes):
        angle = 2 * math.pi * i / n
        x = math.cos(angle)
        y = math.sin(angle)
        positions[node] = (x, y)

    return positions


def get_edges(graph):
    edges = set()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            edge = tuple(sorted([node, neighbor]))
            edges.add(edge)
    return list(edges)


def bfs_traversal(graph, start_node):
    if start_node not in graph:
        return []

    steps = []
    visited = set()
    visited_so_far = []
    queue = [start_node]
    visited.add(start_node)

    while queue:
        node = queue.pop(0)
        visited_so_far.append(node)

        steps.append({
            "visited_node": node,
            "visited_so_far": visited_so_far.copy()
        })

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return steps


def dfs_traversal(graph, start_node):
    if start_node not in graph:
        return []

    steps = []
    visited = set()
    visited_so_far = []

    def _dfs(node):
        if node in visited:
            return
        visited.add(node)
        visited_so_far.append(node)
        steps.append({
            "visited_node": node,
            "visited_so_far": visited_so_far.copy()
        })
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                _dfs(neighbor)

    _dfs(start_node)

    return steps
