"""
Main Streamlit app — entry point.
Teen modes: Sorting (Bubble/Merge/Quick), Tree (BFS/DFS), Graph (BFS/DFS).
- Next/Previous se manual step control
- AI explanation SIRF EK BAAR — button click pe, har step pe nahi
"""

import streamlit as st
from algorithms.sorting import bubble_sort, merge_sort, quick_sort
from algorithms.trees import build_tree_from_list, bfs_traversal as tree_bfs, dfs_traversal as tree_dfs
from algorithms.graphs import build_graph_positions, get_edges, bfs_traversal as graph_bfs, dfs_traversal as graph_dfs
from visualizer.chart_utils import create_bar_chart, create_tree_chart, create_graph_chart
from ai.explainer import explain_algorithm

MAX_ARRAY_SIZE = 15

st.set_page_config(page_title="DSA Visualizer + AI Explainer", page_icon="📊", layout="wide")
st.title("📊 DSA Visualizer + AI Explainer")

mode = st.radio("Kya visualize karna hai?", ["Sorting", "Tree Traversal", "Graph Traversal"], horizontal=True)

with st.sidebar:
    st.header("⚙️ Settings")
    ai_enabled = st.checkbox("🤖 AI Explainer chalu rakho", value=True)


def render_navigation(total_steps):
    current = st.session_state.current_step
    nav_col1, nav_col2, _ = st.columns([1, 1, 3])
    with nav_col1:
        if st.button("◀️ Previous", disabled=(current == 0)):
            st.session_state.current_step -= 1
            st.rerun()
    with nav_col2:
        if st.button("Next ▶️", disabled=(current == total_steps - 1)):
            st.session_state.current_step += 1
            st.rerun()
    st.caption(f"Step {current + 1} of {total_steps}")


def render_ai_panel():
    st.subheader("🤖 AI Explanation")
    if not ai_enabled:
        st.caption("AI Explainer band hai (sidebar se chalu karo).")
        return
    if "ai_explanation" in st.session_state and st.session_state.ai_explanation:
        st.info(st.session_state.ai_explanation)
    else:
        st.caption("Algorithm run karo — AI explanation yahan dikhegi.")


if mode == "Sorting":
    st.write("Algorithm select karo, array do, aur Next/Previous se step-by-step sorting dekho.")

    algorithm = st.selectbox("Algorithm choose karo:", ["Bubble Sort", "Merge Sort", "Quick Sort"])
    user_input = st.text_input("Array enter karo (comma se separate karo):", value="5, 2, 8, 1, 9")

    if st.button("▶️ Sort Karo", type="primary"):
        if not user_input.strip():
            st.warning("Pehle array enter karo.")
        else:
            try:
                arr = [int(x.strip()) for x in user_input.split(",") if x.strip() != ""]
                if len(arr) < 2:
                    st.warning("Kam se kam 2 numbers daalo.")
                elif len(arr) > MAX_ARRAY_SIZE:
                    st.warning(f"Max {MAX_ARRAY_SIZE} numbers allowed.")
                else:
                    if algorithm == "Bubble Sort":
                        steps = bubble_sort(arr)
                    elif algorithm == "Merge Sort":
                        steps = merge_sort(arr)
                    else:
                        steps = quick_sort(arr)

                    final_sorted = steps[-1]["array"]
                    st.session_state.sort_steps = steps
                    st.session_state.sort_algorithm = algorithm
                    st.session_state.current_step = 0
                    st.session_state.active_mode = "Sorting"

                    if ai_enabled:
                        with st.spinner("AI explanation generate ho rahi hai..."):
                            st.session_state.ai_explanation = explain_algorithm(
                                algorithm_name=algorithm,
                                input_data=arr,
                                result=final_sorted
                            )
                    else:
                        st.session_state.ai_explanation = ""

            except ValueError:
                st.error("Sirf numbers daalo, comma se separate karke. Example: 5, 2, 8, 1, 9")

    if st.session_state.get("active_mode") == "Sorting" and "sort_steps" in st.session_state:
        steps = st.session_state.sort_steps
        current = st.session_state.current_step
        step_data = steps[current]
        st.divider()
        col1, col2 = st.columns([2, 1])
        with col1:
            fig = create_bar_chart(step_data["array"], step_data["comparing"], step_data["swapped"])
            st.pyplot(fig)
            render_navigation(len(steps))
        with col2:
            render_ai_panel()


elif mode == "Tree Traversal":
    st.write("Tree banao, traversal choose karo, aur Next/Previous se step-by-step dekho.")

    traversal_type = st.selectbox("Traversal type:", ["BFS (Level Order)", "DFS (Preorder)"])
    tree_input = st.text_input(
        "Tree values enter karo (level-order, comma se separate):",
        value="5, 3, 8, 1, 4, 7, 9"
    )
    st.caption("5 root hai, 3 aur 8 uske children, 1 aur 4 teen ke children, etc.")

    if st.button("🌳 Traverse Karo", type="primary"):
        try:
            values = [int(x.strip()) for x in tree_input.split(",") if x.strip() != ""]
            if len(values) == 0:
                st.warning("Kam se kam 1 value daalo.")
            elif len(values) > MAX_ARRAY_SIZE:
                st.warning(f"Max {MAX_ARRAY_SIZE} values allowed.")
            else:
                root = build_tree_from_list(values)
                if traversal_type == "BFS (Level Order)":
                    steps, positions, edges = tree_bfs(root)
                else:
                    steps, positions, edges = tree_dfs(root)

                traversal_order = [s["visited_value"] for s in steps]
                st.session_state.tree_steps = steps
                st.session_state.tree_positions = positions
                st.session_state.tree_edges = edges
                st.session_state.current_step = 0
                st.session_state.active_mode = "Tree Traversal"

                if ai_enabled:
                    with st.spinner("AI explanation generate ho rahi hai..."):
                        st.session_state.ai_explanation = explain_algorithm(
                            algorithm_name=f"Tree {traversal_type}",
                            input_data=f"Tree nodes (level-order): {values}",
                            result=f"Traversal order: {traversal_order}"
                        )
                else:
                    st.session_state.ai_explanation = ""

        except ValueError:
            st.error("Sirf numbers daalo, comma se separate karke.")

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
                visited_so_far=step_data["visited_so_far"][:-1]
            )
            st.pyplot(fig)
            render_navigation(len(steps))
        with col2:
            render_ai_panel()


elif mode == "Graph Traversal":
    st.write("Graph define karo, traversal choose karo, aur step-by-step dekho.")

    traversal_type = st.selectbox("Traversal type:", ["BFS", "DFS"])
    st.caption("Format: har line mein 'Node: Neighbor1, Neighbor2'")
    graph_input = st.text_area(
        "Graph define karo:",
        value="A: B, C\nB: A, D\nC: A, D\nD: B, C, E\nE: D",
        height=150
    )
    start_node = st.text_input("Start node:", value="A")

    if st.button("🔗 Traverse Karo", type="primary"):
        try:
            graph = {}
            for line in graph_input.strip().split("\n"):
                if ":" not in line:
                    continue
                node, neighbors_str = line.split(":", 1)
                node = node.strip()
                neighbors = [n.strip() for n in neighbors_str.split(",") if n.strip()]
                graph[node] = neighbors

            if not graph:
                st.warning("Graph khaali hai — sahi format mein likho.")
            elif start_node.strip() not in graph:
                st.warning(f"'{start_node}' graph mein nahi mila.")
            else:
                positions = build_graph_positions(graph)
                edges = get_edges(graph)

                if traversal_type == "BFS":
                    steps = graph_bfs(graph, start_node.strip())
                else:
                    steps = graph_dfs(graph, start_node.strip())

                traversal_order = [s["visited_node"] for s in steps]
                st.session_state.graph_steps = steps
                st.session_state.graph_positions = positions
                st.session_state.graph_edges = edges
                st.session_state.current_step = 0
                st.session_state.active_mode = "Graph Traversal"

                if ai_enabled:
                    with st.spinner("AI explanation generate ho rahi hai..."):
                        st.session_state.ai_explanation = explain_algorithm(
                            algorithm_name=f"Graph {traversal_type}",
                            input_data=f"Graph nodes: {list(graph.keys())}, Start: {start_node.strip()}",
                            result=f"Traversal order: {traversal_order}"
                        )
                else:
                    st.session_state.ai_explanation = ""

        except Exception:
            st.error("Graph format galat hai. Example: 'A: B, C'")

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
                visited_so_far=step_data["visited_so_far"][:-1]
            )
            st.pyplot(fig)
            render_navigation(len(steps))
        with col2:
            render_ai_panel()
