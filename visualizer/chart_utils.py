"""
Matplotlib se charts banane wale helper functions — bar chart (sorting),
tree chart, aur graph chart.
"""

import matplotlib.pyplot as plt


def create_bar_chart(array, comparing=None, swapped=False):
    fig, ax = plt.subplots(figsize=(8, 4))

    colors = ["#4ecdc4"] * len(array)

    if comparing:
        i, j = comparing
        highlight_color = "#ff6b6b" if swapped else "#ffa552"
        colors[i] = highlight_color
        colors[j] = highlight_color

    ax.bar(range(len(array)), array, color=colors)
    ax.set_xticks(range(len(array)))
    ax.set_xticklabels(array)
    ax.set_ylim(0, max(array) * 1.2)
    ax.set_yticks([])

    return fig


def create_tree_chart(positions, edges, visited_id=None, visited_so_far=None):
    visited_so_far = visited_so_far or []
    fig, ax = plt.subplots(figsize=(8, 5))

    for parent_id, child_id in edges:
        x1, y1, _ = positions[parent_id]
        x2, y2, _ = positions[child_id]
        ax.plot([x1, x2], [y1, y2], color="#4a4a6a", zorder=1, linewidth=1.5)

    for nid, (x, y, value) in positions.items():
        if nid == visited_id:
            color = "#ff6b6b"
        elif nid in visited_so_far:
            color = "#6bcb77"
        else:
            color = "#4ecdc4"

        ax.scatter(x, y, s=1200, color=color, zorder=2, edgecolors="white", linewidths=1.5)
        ax.text(x, y, str(value), ha="center", va="center", fontsize=12, fontweight="bold", zorder=3, color="black")

    ax.set_xlim(-0.1, 1.1)
    ax.axis("off")

    return fig


def create_graph_chart(positions, edges, visited_node=None, visited_so_far=None):
    visited_so_far = visited_so_far or []
    fig, ax = plt.subplots(figsize=(6, 6))

    for node_a, node_b in edges:
        x1, y1 = positions[node_a]
        x2, y2 = positions[node_b]
        ax.plot([x1, x2], [y1, y2], color="#4a4a6a", zorder=1, linewidth=1.5)

    for label, (x, y) in positions.items():
        if label == visited_node:
            color = "#ff6b6b"
        elif label in visited_so_far:
            color = "#6bcb77"
        else:
            color = "#4ecdc4"

        ax.scatter(x, y, s=1200, color=color, zorder=2, edgecolors="white", linewidths=1.5)
        ax.text(x, y, str(label), ha="center", va="center", fontsize=12, fontweight="bold", zorder=3, color="black")

    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.4, 1.4)
    ax.set_aspect("equal")
    ax.axis("off")

    return fig
