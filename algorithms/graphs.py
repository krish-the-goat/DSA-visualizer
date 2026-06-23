"""
Graph traversal logic — BFS and DFS.
Graph is represented as an adjacency list (dict).

Each step dict contains:
  - visited_node: the node label currently being visited
  - visited_so_far: list of all visited node labels so far
  - caption: human-readable step description
  - pseudo_line: int for pseudo-code highlighting
"""

import math


def build_graph_positions(graph):
    """Arranges graph nodes in a circle for visualization."""
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
    """Extracts unique edges from the adjacency list."""
    edges = set()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            edge = tuple(sorted([node, neighbor]))
            edges.add(edge)
    return list(edges)


def bfs_traversal(graph, start_node):
    """
    BFS traversal with step-by-step tracking.
    Returns list of step dicts.
    """
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

        # Find unvisited neighbors that will be added to queue
        new_neighbors = [
            n for n in graph.get(node, []) if n not in visited
        ]
        queue_after = list(queue) + new_neighbors

        steps.append({
            "visited_node": node,
            "visited_so_far": visited_so_far.copy(),
            "caption": (
                f"Visiting node {node}. "
                f"Neighbors: {graph.get(node, [])}. "
                f"Adding {new_neighbors if new_neighbors else 'none'} to queue. "
                f"Queue: {queue_after if queue_after else '[]'}"
            ),
            "pseudo_line": 4,
        })

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return steps


def dfs_traversal(graph, start_node):
    """
    DFS traversal with step-by-step tracking.
    Returns list of step dicts.
    """
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

        unvisited = [n for n in graph.get(node, []) if n not in visited]

        if unvisited:
            next_action = f"Exploring neighbor {unvisited[0]} next."
        else:
            next_action = "No unvisited neighbors — backtracking."

        steps.append({
            "visited_node": node,
            "visited_so_far": visited_so_far.copy(),
            "caption": (
                f"Visiting node {node}. "
                f"Neighbors: {graph.get(node, [])}. "
                f"Unvisited: {unvisited if unvisited else 'none'}. "
                f"{next_action}"
            ),
            "pseudo_line": 3,
        })

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                _dfs(neighbor)

    _dfs(start_node)

    return steps
