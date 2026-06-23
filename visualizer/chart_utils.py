"""
Matplotlib chart helpers — bar chart (sorting), tree chart, graph chart.
All charts use a dark theme to match the app's premium aesthetic.
Memory-safe: figures are created fresh each call with plt.close() in callers.
"""

import matplotlib.pyplot as plt


# ─── Color Palette ────────────────────────────────────────────────────────────

BG_COLOR = "#0f0f1a"
CARD_BG = "#1a1a2e"
DEFAULT_BAR = "#4ecdc4"
COMPARING_COLOR = "#ffa552"
SWAPPED_COLOR = "#ff6b9d"
DONE_COLOR = "#4ade80"
NODE_DEFAULT = "#2d2d5e"
NODE_VISITING = "#ff6b9d"
NODE_VISITED = "#4ade80"
EDGE_COLOR = "#3a3a5c"
TEXT_COLOR = "#e8e8f0"
LABEL_COLOR = "#a0a0b8"

# Gradient palette for bars (cyan → purple)
BAR_GRADIENT = [
    "#00d2ff", "#1ac8f0", "#33bee0", "#4db4d1",
    "#66aac2", "#7fa0b3", "#9996a3", "#b28c94",
    "#cc8285", "#e57876", "#ff6e66",
]


def _get_bar_color(index: int, total: int) -> str:
    """Returns a gradient color for a bar based on its position."""
    if total <= 1:
        return BAR_GRADIENT[0]
    ratio = index / (total - 1)
    color_idx = int(ratio * (len(BAR_GRADIENT) - 1))
    return BAR_GRADIENT[min(color_idx, len(BAR_GRADIENT) - 1)]


def create_bar_chart(array, comparing=None, swapped=False):
    """
    Creates a dark-themed bar chart for sorting visualization.
    - comparing: tuple (i, j) of indices being compared
    - swapped: True if a swap occurred at this step
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    n = len(array)
    colors = [_get_bar_color(i, n) for i in range(n)]
    edge_colors = ["none"] * n
    edge_widths = [0] * n

    if comparing:
        i, j = comparing
        highlight = SWAPPED_COLOR if swapped else COMPARING_COLOR
        if 0 <= i < n:
            colors[i] = highlight
            edge_colors[i] = highlight
            edge_widths[i] = 2
        if 0 <= j < n:
            colors[j] = highlight
            edge_colors[j] = highlight
            edge_widths[j] = 2
    elif comparing is None:
        # Final step — all bars are "done" green
        colors = [DONE_COLOR] * n

    bars = ax.bar(
        range(n), array, color=colors,
        edgecolor=edge_colors, linewidth=edge_widths,
        width=0.7, zorder=2
    )

    # Glow effect for highlighted bars
    if comparing:
        i, j = comparing
        highlight = SWAPPED_COLOR if swapped else COMPARING_COLOR
        for idx in [i, j]:
            if 0 <= idx < n:
                ax.bar(
                    idx, array[idx], color=highlight, alpha=0.15,
                    width=1.0, zorder=1
                )

    # Value labels on bars
    max_val = max(array)
    min_val = min(array)
    val_range = max(max_val - min_val, 1)  # Prevent division by zero
    label_offset = val_range * 0.03

    for idx, (bar_obj, val) in enumerate(zip(bars, array)):
        # Place label above bar for positive, below for negative
        if val >= 0:
            label_y = val + label_offset
            va = "bottom"
        else:
            label_y = val - label_offset
            va = "top"
        ax.text(
            bar_obj.get_x() + bar_obj.get_width() / 2, label_y,
            str(val), ha="center", va=va,
            fontsize=11, fontweight="bold", color=TEXT_COLOR,
            fontfamily="sans-serif"
        )

    # Index labels below
    ax.set_xticks(range(n))
    ax.set_xticklabels(
        [str(i) for i in range(n)],
        fontsize=9, color=LABEL_COLOR, fontfamily="sans-serif"
    )

    # Compute safe y-axis limits
    y_bottom = min(min_val, 0) - val_range * 0.15
    y_top = max(max_val, 0) + val_range * 0.25
    if y_bottom == y_top:
        y_bottom -= 1
        y_top += 1
    ax.set_ylim(y_bottom, y_top)
    ax.set_yticks([])

    # Remove spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.tick_params(axis="x", colors=LABEL_COLOR, length=0)
    fig.tight_layout(pad=1.0)

    return fig


def create_tree_chart(positions, edges, visited_id=None, visited_so_far=None):
    """
    Creates a dark-themed tree visualization.
    - visited_id: the node currently being visited (highlighted)
    - visited_so_far: list of previously visited node IDs
    """
    visited_so_far = visited_so_far or []
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    # Draw edges
    for parent_id, child_id in edges:
        x1, y1, _ = positions[parent_id]
        x2, y2, _ = positions[child_id]

        # Color edge if both nodes are visited
        if parent_id in visited_so_far and child_id in visited_so_far:
            edge_color = NODE_VISITED
            alpha = 0.6
            lw = 2.5
        elif parent_id == visited_id or child_id == visited_id:
            edge_color = NODE_VISITING
            alpha = 0.5
            lw = 2.5
        else:
            edge_color = EDGE_COLOR
            alpha = 0.5
            lw = 1.5

        ax.plot(
            [x1, x2], [y1, y2],
            color=edge_color, alpha=alpha, linewidth=lw, zorder=1,
            solid_capstyle="round"
        )

    # Draw nodes
    for nid, (x, y, value) in positions.items():
        if nid == visited_id:
            color = NODE_VISITING
            size = 1600
            # Glow effect
            ax.scatter(x, y, s=2400, color=NODE_VISITING, alpha=0.15, zorder=1.5)
        elif nid in visited_so_far:
            color = NODE_VISITED
            size = 1400
        else:
            color = NODE_DEFAULT
            size = 1200

        ax.scatter(
            x, y, s=size, color=color, zorder=2,
            edgecolors=(1, 1, 1, 0.2), linewidths=2
        )
        ax.text(
            x, y, str(value),
            ha="center", va="center",
            fontsize=13, fontweight="bold", zorder=3,
            color="white", fontfamily="sans-serif"
        )

    ax.set_xlim(-0.15, 1.15)
    y_vals = [pos[1] for pos in positions.values()]
    if y_vals:
        ax.set_ylim(min(y_vals) - 0.5, max(y_vals) + 0.5)
    ax.axis("off")
    fig.tight_layout(pad=0.5)

    return fig


def create_graph_chart(positions, edges, visited_node=None, visited_so_far=None):
    """
    Creates a dark-themed graph visualization.
    - visited_node: the node currently being visited
    - visited_so_far: list of previously visited node labels
    """
    visited_so_far = visited_so_far or []
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    # Draw edges
    for node_a, node_b in edges:
        x1, y1 = positions[node_a]
        x2, y2 = positions[node_b]

        if node_a in visited_so_far and node_b in visited_so_far:
            edge_color = NODE_VISITED
            alpha = 0.6
            lw = 2.5
        elif node_a == visited_node or node_b == visited_node:
            edge_color = NODE_VISITING
            alpha = 0.5
            lw = 2.5
        else:
            edge_color = EDGE_COLOR
            alpha = 0.5
            lw = 1.5

        ax.plot(
            [x1, x2], [y1, y2],
            color=edge_color, alpha=alpha, linewidth=lw, zorder=1,
            solid_capstyle="round"
        )

    # Draw nodes
    for label, (x, y) in positions.items():
        if label == visited_node:
            color = NODE_VISITING
            size = 1600
            ax.scatter(x, y, s=2400, color=NODE_VISITING, alpha=0.15, zorder=1.5)
        elif label in visited_so_far:
            color = NODE_VISITED
            size = 1400
        else:
            color = NODE_DEFAULT
            size = 1200

        ax.scatter(
            x, y, s=size, color=color, zorder=2,
            edgecolors=(1, 1, 1, 0.2), linewidths=2
        )
        ax.text(
            x, y, str(label),
            ha="center", va="center",
            fontsize=13, fontweight="bold", zorder=3,
            color="white", fontfamily="sans-serif"
        )

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout(pad=0.5)

    return fig
