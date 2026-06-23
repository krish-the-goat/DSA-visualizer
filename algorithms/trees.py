"""
Binary Tree traversal logic — BFS (level order) aur DFS (preorder).
Node IDs ek hi central function (_assign_ids) se aate hain,
taaki positions, edges, aur traversal steps mein SAME id consistently
use ho.
"""


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def build_tree_from_list(values):
    if not values or values[0] is None:
        return None

    root = TreeNode(values[0])
    queue = [root]
    i = 1

    while i < len(values) and queue:
        current = queue.pop(0)

        if i < len(values) and values[i] is not None:
            current.left = TreeNode(values[i])
            queue.append(current.left)
        i += 1

        if i < len(values) and values[i] is not None:
            current.right = TreeNode(values[i])
            queue.append(current.right)
        i += 1

    return root


def _assign_ids(root):
    if root is None:
        return {}

    node_to_id = {}
    counter = 0
    queue = [root]
    while queue:
        node = queue.pop(0)
        if id(node) in node_to_id:
            continue
        node_to_id[id(node)] = counter
        counter += 1
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return node_to_id


def tree_to_positions(root, node_to_id):
    if root is None:
        return {}, []

    positions = {}
    edges = []

    levels = []
    queue = [root]
    while queue:
        level_nodes = []
        next_queue = []
        for node in queue:
            level_nodes.append(node)
            if node.left:
                next_queue.append(node.left)
            if node.right:
                next_queue.append(node.right)
        levels.append(level_nodes)
        queue = next_queue

    for depth, level_nodes in enumerate(levels):
        n = len(level_nodes)
        for idx, node in enumerate(level_nodes):
            x = (idx + 1) / (n + 1)
            y = -depth
            nid = node_to_id[id(node)]
            positions[nid] = (x, y, node.value)

    def collect_edges(node):
        if node is None:
            return
        nid = node_to_id[id(node)]
        if node.left:
            edges.append((nid, node_to_id[id(node.left)]))
            collect_edges(node.left)
        if node.right:
            edges.append((nid, node_to_id[id(node.right)]))
            collect_edges(node.right)

    collect_edges(root)

    return positions, edges


def bfs_traversal(root):
    if root is None:
        return [], {}, []

    node_to_id = _assign_ids(root)
    positions, edges = tree_to_positions(root, node_to_id)

    steps = []
    visited_so_far = []
    queue = [root]
    visited_set = set()

    while queue:
        node = queue.pop(0)
        nid = node_to_id[id(node)]

        if nid in visited_set:
            continue
        visited_set.add(nid)
        visited_so_far.append(nid)

        steps.append({
            "visited_id": nid,
            "visited_value": node.value,
            "visited_so_far": visited_so_far.copy()
        })

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return steps, positions, edges


def dfs_traversal(root):
    if root is None:
        return [], {}, []

    node_to_id = _assign_ids(root)
    positions, edges = tree_to_positions(root, node_to_id)

    steps = []
    visited_so_far = []

    def _dfs(node):
        if node is None:
            return
        nid = node_to_id[id(node)]
        visited_so_far.append(nid)
        steps.append({
            "visited_id": nid,
            "visited_value": node.value,
            "visited_so_far": visited_so_far.copy()
        })
        _dfs(node.left)
        _dfs(node.right)

    _dfs(root)

    return steps, positions, edges
