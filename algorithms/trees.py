"""
Binary Tree traversal logic — BFS (level order) and DFS (preorder).
Node IDs are assigned via a central function (_assign_ids) to ensure
consistent IDs across positions, edges, and traversal steps.

Each step dict contains:
  - visited_id, visited_value, visited_so_far (existing)
  - caption: human-readable step description
  - pseudo_line: int for pseudo-code highlighting
"""


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def build_tree_from_list(values):
    """Builds a binary tree from a level-order list of values."""
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
    """Assigns unique integer IDs to nodes via BFS traversal."""
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
    """Computes (x, y) positions for each node for visualization."""
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


def _get_children_desc(node):
    """Returns a description of a node's children for captions."""
    children = []
    if node.left:
        children.append(str(node.left.value))
    if node.right:
        children.append(str(node.right.value))
    if children:
        return f"Children: [{', '.join(children)}]"
    return "No children (leaf node)"


def bfs_traversal(root):
    """
    BFS (level-order) traversal with step-by-step tracking.
    Returns (steps, positions, edges).
    """
    if root is None:
        return [], {}, []

    node_to_id = _assign_ids(root)
    positions, edges = tree_to_positions(root, node_to_id)

    steps = []
    visited_so_far = []
    queue = [root]
    visited_set = set()
    level_map = {id(root): 0}

    while queue:
        node = queue.pop(0)
        nid = node_to_id[id(node)]

        if nid in visited_set:
            continue
        visited_set.add(nid)
        visited_so_far.append(nid)

        level = level_map.get(id(node), 0)
        children_desc = _get_children_desc(node)
        queue_preview = [n.value for n in queue]

        steps.append({
            "visited_id": nid,
            "visited_value": node.value,
            "visited_so_far": visited_so_far.copy(),
            "caption": (
                f"Visiting node {node.value} (Level {level}). "
                f"{children_desc}. Queue: {queue_preview if queue_preview else '[]'}"
            ),
            "pseudo_line": 4,
        })

        if node.left:
            queue.append(node.left)
            level_map[id(node.left)] = level + 1
        if node.right:
            queue.append(node.right)
            level_map[id(node.right)] = level + 1

    return steps, positions, edges


def dfs_traversal(root):
    """
    DFS (preorder) traversal with step-by-step tracking.
    Returns (steps, positions, edges).
    """
    if root is None:
        return [], {}, []

    node_to_id = _assign_ids(root)
    positions, edges = tree_to_positions(root, node_to_id)

    steps = []
    visited_so_far = []
    depth_map = {id(root): 0}

    def _dfs(node):
        if node is None:
            return
        nid = node_to_id[id(node)]
        visited_so_far.append(nid)

        depth = depth_map.get(id(node), 0)
        children_desc = _get_children_desc(node)

        next_action = ""
        if node.left:
            next_action = f"Going deeper to left child {node.left.value}."
            depth_map[id(node.left)] = depth + 1
        elif node.right:
            next_action = f"No left child. Going to right child {node.right.value}."
            depth_map[id(node.right)] = depth + 1
        else:
            next_action = "Leaf node — backtracking."

        if node.right and node.left:
            depth_map[id(node.right)] = depth + 1

        steps.append({
            "visited_id": nid,
            "visited_value": node.value,
            "visited_so_far": visited_so_far.copy(),
            "caption": (
                f"Visiting node {node.value} (Depth {depth}). "
                f"{children_desc}. {next_action}"
            ),
            "pseudo_line": 3,
        })

        _dfs(node.left)
        _dfs(node.right)

    _dfs(root)

    return steps, positions, edges
