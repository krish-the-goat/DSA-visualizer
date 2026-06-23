"""
Main Streamlit app — DSA Visualizer + AI Explainer.
Modes: Sorting (Bubble/Merge/Quick/Insertion/Selection), Tree (BFS/DFS), Graph (BFS/DFS).
Features: Step-by-step navigation, auto-play, pseudo-code highlighting, AI explanation.
"""

import time
import streamlit as st
import matplotlib.pyplot as plt

from custom_theme import inject_custom_css
from security import (
    sanitize_array_input,
    sanitize_tree_input,
    sanitize_graph_input,
    sanitize_node_label,
    check_ai_rate_limit,
    get_ai_calls_remaining,
)
from algorithms.sorting import (
    bubble_sort, merge_sort, quick_sort,
    insertion_sort, selection_sort,
    generate_random_array,
)
from algorithms.trees import (
    build_tree_from_list,
    bfs_traversal as tree_bfs,
    dfs_traversal as tree_dfs,
)
from algorithms.graphs import (
    build_graph_positions,
    get_edges,
    bfs_traversal as graph_bfs,
    dfs_traversal as graph_dfs,
)
from visualizer.chart_utils import create_bar_chart, create_tree_chart, create_graph_chart
from visualizer.pseudocode import render_pseudocode
from ai.explainer import explain_algorithm


# ─── Page Config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="DSA Visualizer — Learn Algorithms Visually",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()

st.title("📊 DSA Visualizer + AI Explainer")

mode = st.radio(
    "What do you want to visualize?",
    ["Sorting", "Tree Traversal", "Graph Traversal"],
    horizontal=True,
)


# ─── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.header("⚙️ Settings")
    ai_enabled = st.checkbox("🤖 Enable AI Explainer", value=True)

    if ai_enabled:
        remaining = get_ai_calls_remaining()
        st.markdown(
            f'<span class="rate-badge">AI calls remaining: {remaining}</span>',
            unsafe_allow_html=True,
        )

    st.divider()

    st.subheader("▶️ Playback")
    speed_label = st.select_slider(
        "Auto-play speed",
        options=["Slow", "Normal", "Fast"],
        value="Normal",
    )
    speed_map = {"Slow": 1.0, "Normal": 0.5, "Fast": 0.2}
    play_speed = speed_map[speed_label]

    st.divider()

    if st.button("🔄 Reset Everything", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ─── Helper Functions ─────────────────────────────────────────────────────────

def render_navigation(total_steps):
    """Renders Previous / Auto Play / Next navigation controls."""
    current = st.session_state.current_step
    is_playing = st.session_state.get("auto_playing", False)

    col_prev, col_play, col_next, col_info = st.columns([1, 1, 1, 2])

    with col_prev:
        if st.button("◀️ Previous", disabled=(current == 0 or is_playing), key="btn_prev"):
            st.session_state.current_step -= 1
            st.rerun()

    with col_play:
        if is_playing:
            if st.button("⏸️ Pause", key="btn_pause"):
                st.session_state.auto_playing = False
                st.rerun()
        else:
            if st.button("▶️ Auto Play", disabled=(current >= total_steps - 1), key="btn_play"):
                st.session_state.auto_playing = True
                st.rerun()

    with col_next:
        if st.button("Next ▶️", disabled=(current >= total_steps - 1 or is_playing), key="btn_next"):
            st.session_state.current_step += 1
            st.rerun()

    with col_info:
        progress = (current + 1) / total_steps
        st.progress(progress)
        st.markdown(
            f'<div class="step-progress">Step {current + 1} of {total_steps}</div>',
            unsafe_allow_html=True,
        )


def render_step_caption(caption: str):
    """Renders the step caption in a styled card."""
    st.markdown(
        f'<div class="step-caption animate-fade">'
        f'<span class="step-icon">💡</span>{caption}'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_right_panel(algorithm_name: str, pseudo_line: int):
    """Renders the tabbed right panel with Pseudo Code and AI Explanation."""
    tab_pseudo, tab_ai = st.tabs(["📝 Pseudo Code", "🤖 AI Explanation"])

    with tab_pseudo:
        render_pseudocode(algorithm_name, pseudo_line)

    with tab_ai:
        if not ai_enabled:
            st.caption("AI Explainer is disabled. Enable it in the sidebar.")
        elif "ai_explanation" in st.session_state and st.session_state.ai_explanation:
            st.markdown(
                f'<div class="ai-card">{st.session_state.ai_explanation}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.caption("Run an algorithm to see the AI explanation here.")


def handle_auto_play(total_steps):
    """Handles auto-play logic — advances one step and reruns."""
    if st.session_state.get("auto_playing", False):
        current = st.session_state.current_step
        if current < total_steps - 1:
            time.sleep(play_speed)
            st.session_state.current_step += 1
            st.rerun()
        else:
            st.session_state.auto_playing = False


def display_chart(fig):
    """Displays a matplotlib figure and properly closes it."""
    st.pyplot(fig)
    plt.close(fig)


# ─── Sorting Mode ─────────────────────────────────────────────────────────────

if mode == "Sorting":
    st.write("Select an algorithm, enter an array, and step through the sorting process.")

    algorithm = st.selectbox(
        "Choose algorithm:",
        ["Bubble Sort", "Merge Sort", "Quick Sort", "Insertion Sort", "Selection Sort"],
    )

    col_input, col_random = st.columns([4, 1])
    with col_input:
        user_input = st.text_input(
            "Enter array (comma-separated numbers):",
            value=st.session_state.get("sort_input_value", "5, 2, 8, 1, 9"),
            key="sort_input",
        )
    with col_random:
        st.write("")  # spacing
        st.write("")
        if st.button("🎲 Random", key="btn_random_sort"):
            random_arr = generate_random_array()
            st.session_state.sort_input_value = ", ".join(str(x) for x in random_arr)
            st.rerun()

    if st.button("▶️ Sort", type="primary"):
        try:
            arr = sanitize_array_input(user_input)

            algo_map = {
                "Bubble Sort": bubble_sort,
                "Merge Sort": merge_sort,
                "Quick Sort": quick_sort,
                "Insertion Sort": insertion_sort,
                "Selection Sort": selection_sort,
            }
            steps = algo_map[algorithm](arr)
            final_sorted = steps[-1]["array"]

            st.session_state.sort_steps = steps
            st.session_state.sort_algorithm = algorithm
            st.session_state.current_step = 0
            st.session_state.active_mode = "Sorting"
            st.session_state.auto_playing = False

            if ai_enabled and check_ai_rate_limit():
                with st.spinner("Generating AI explanation..."):
                    st.session_state.ai_explanation = explain_algorithm(
                        algorithm_name=algorithm,
                        input_data=arr,
                        result=final_sorted,
                    )
            else:
                st.session_state.ai_explanation = ""

        except ValueError as e:
            st.error(str(e))

    if st.session_state.get("active_mode") == "Sorting" and "sort_steps" in st.session_state:
        steps = st.session_state.sort_steps
        current = st.session_state.current_step
        step_data = steps[current]

        st.divider()

        col1, col2 = st.columns([2, 1])

        with col1:
            fig = create_bar_chart(step_data["array"], step_data["comparing"], step_data["swapped"])
            display_chart(fig)
            render_step_caption(step_data.get("caption", ""))
            render_navigation(len(steps))

        with col2:
            render_right_panel(
                st.session_state.sort_algorithm,
                step_data.get("pseudo_line", 0),
            )

        handle_auto_play(len(steps))


# ─── Tree Traversal Mode ─────────────────────────────────────────────────────

elif mode == "Tree Traversal":
    st.write("Build a tree, choose a traversal type, and step through it.")

    traversal_type = st.selectbox("Traversal type:", ["BFS (Level Order)", "DFS (Preorder)"])
    tree_input = st.text_input(
        "Enter tree values (level-order, comma-separated):",
        value="5, 3, 8, 1, 4, 7, 9",
    )
    st.caption("5 is root, 3 and 8 are its children, 1 and 4 are children of 3, etc.")

    if st.button("🌳 Traverse", type="primary"):
        try:
            values = sanitize_tree_input(tree_input)

            root = build_tree_from_list(values)
            if traversal_type == "BFS (Level Order)":
                steps, positions, edges = tree_bfs(root)
                algo_name = "Tree BFS (Level Order)"
            else:
                steps, positions, edges = tree_dfs(root)
                algo_name = "Tree DFS (Preorder)"

            traversal_order = [s["visited_value"] for s in steps]
            st.session_state.tree_steps = steps
            st.session_state.tree_positions = positions
            st.session_state.tree_edges = edges
            st.session_state.tree_algorithm = algo_name
            st.session_state.current_step = 0
            st.session_state.active_mode = "Tree Traversal"
            st.session_state.auto_playing = False

            if ai_enabled and check_ai_rate_limit():
                with st.spinner("Generating AI explanation..."):
                    st.session_state.ai_explanation = explain_algorithm(
                        algorithm_name=algo_name,
                        input_data=f"Tree nodes (level-order): {values}",
                        result=f"Traversal order: {traversal_order}",
                    )
            else:
                st.session_state.ai_explanation = ""

        except ValueError as e:
            st.error(str(e))

    if st.session_state.get("active_mode") == "Tree Traversal" and "tree_steps" in st.session_state:
        steps = st.session_state.tree_steps
        positions = st.session_state.tree_positions
        edges = st.session_state.tree_edges
        current = st.session_state.current_step
        step_data = steps[current]

        st.divider()

        col1, col2 = st.columns([2, 1])

        with col1:
            fig = create_tree_chart(
                positions, edges,
                visited_id=step_data["visited_id"],
                visited_so_far=step_data["visited_so_far"][:-1],
            )
            display_chart(fig)
            render_step_caption(step_data.get("caption", ""))
            render_navigation(len(steps))

        with col2:
            render_right_panel(
                st.session_state.tree_algorithm,
                step_data.get("pseudo_line", 0),
            )

        handle_auto_play(len(steps))


# ─── Graph Traversal Mode ────────────────────────────────────────────────────

elif mode == "Graph Traversal":
    st.write("Define a graph, choose a traversal type, and step through it.")

    traversal_type = st.selectbox("Traversal type:", ["BFS", "DFS"])
    st.caption("Format: each line as 'Node: Neighbor1, Neighbor2'")
    graph_input = st.text_area(
        "Define your graph:",
        value="A: B, C\nB: A, D\nC: A, D\nD: B, C, E\nE: D",
        height=150,
    )
    start_node = st.text_input("Start node:", value="A")

    if st.button("🔗 Traverse", type="primary"):
        try:
            graph = sanitize_graph_input(graph_input)
            validated_start = sanitize_node_label(start_node)

            if validated_start not in graph:
                st.warning(f"'{validated_start}' not found in the graph.")
            else:
                positions = build_graph_positions(graph)
                edges = get_edges(graph)

                if traversal_type == "BFS":
                    steps = graph_bfs(graph, validated_start)
                    algo_name = "Graph BFS"
                else:
                    steps = graph_dfs(graph, validated_start)
                    algo_name = "Graph DFS"

                traversal_order = [s["visited_node"] for s in steps]
                st.session_state.graph_steps = steps
                st.session_state.graph_positions = positions
                st.session_state.graph_edges = edges
                st.session_state.graph_algorithm = algo_name
                st.session_state.current_step = 0
                st.session_state.active_mode = "Graph Traversal"
                st.session_state.auto_playing = False

                if ai_enabled and check_ai_rate_limit():
                    with st.spinner("Generating AI explanation..."):
                        st.session_state.ai_explanation = explain_algorithm(
                            algorithm_name=algo_name,
                            input_data=f"Graph nodes: {list(graph.keys())}, Start: {validated_start}",
                            result=f"Traversal order: {traversal_order}",
                        )
                else:
                    st.session_state.ai_explanation = ""

        except ValueError as e:
            st.error(str(e))

    if st.session_state.get("active_mode") == "Graph Traversal" and "graph_steps" in st.session_state:
        steps = st.session_state.graph_steps
        positions = st.session_state.graph_positions
        edges = st.session_state.graph_edges
        current = st.session_state.current_step
        step_data = steps[current]

        st.divider()

        col1, col2 = st.columns([2, 1])

        with col1:
            fig = create_graph_chart(
                positions, edges,
                visited_node=step_data["visited_node"],
                visited_so_far=step_data["visited_so_far"][:-1],
            )
            display_chart(fig)
            render_step_caption(step_data.get("caption", ""))
            render_navigation(len(steps))

        with col2:
            render_right_panel(
                st.session_state.graph_algorithm,
                step_data.get("pseudo_line", 0),
            )

        handle_auto_play(len(steps))
