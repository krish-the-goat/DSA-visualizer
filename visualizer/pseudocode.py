"""
Pseudo-code display module — renders algorithm pseudo-code with
the current executing line highlighted.
"""

import streamlit as st

# ─── Pseudo-code definitions ─────────────────────────────────────────────────

PSEUDOCODE = {
    "Bubble Sort": [
        "function bubbleSort(arr):",
        "  for i = 0 to n-1:",
        "    for j = 0 to n-i-2:",
        "      if arr[j] > arr[j+1]:",
        "        swap(arr[j], arr[j+1])",
        "      end if",
        "  return arr  ✅ Sorted!",
    ],
    "Merge Sort": [
        "function mergeSort(arr, left, right):",
        "  if right - left <= 1: return",
        "  mid = (left + right) / 2",
        "  mergeSort(arr, left, mid)",
        "  mergeSort(arr, mid, right)",
        "  while leftHalf and rightHalf:",
        "    if leftHalf[i] <= rightHalf[j]:",
        "      place leftHalf[i]",
        "    else: place rightHalf[j]",
        "  copy remaining elements",
        "  return arr  ✅ Sorted!",
    ],
    "Quick Sort": [
        "function quickSort(arr, low, high):",
        "  if low < high:",
        "    pivotIdx = partition(arr, low, high)",
        "    quickSort(arr, low, pivotIdx-1)",
        "    quickSort(arr, pivotIdx+1, high)",
        "  partition: pivot = arr[high]",
        "    for j = low to high-1:",
        "      if arr[j] < pivot: swap",
        "    place pivot at final position",
        "  return pivotIdx",
        "  return arr  ✅ Sorted!",
    ],
    "Insertion Sort": [
        "function insertionSort(arr):",
        "  arr[0] is sorted",
        "  for i = 1 to n-1:",
        "    key = arr[i], j = i-1",
        "    while j >= 0 and arr[j] > key:",
        "      shift arr[j] → arr[j+1]",
        "    arr[j+1] = key",
        "  return arr  ✅ Sorted!",
    ],
    "Selection Sort": [
        "function selectionSort(arr):",
        "  for i = 0 to n-1:",
        "    minIdx = i",
        "    for j = i+1 to n-1:",
        "      if arr[j] < arr[minIdx]:",
        "        minIdx = j",
        "    swap(arr[i], arr[minIdx])",
        "  return arr  ✅ Sorted!",
    ],
    "Tree BFS (Level Order)": [
        "function treeBFS(root):",
        "  queue = [root]",
        "  while queue is not empty:",
        "    node = queue.dequeue()",
        "    visit(node)",
        "    if node.left: queue.enqueue(left)",
        "    if node.right: queue.enqueue(right)",
    ],
    "Tree DFS (Preorder)": [
        "function treeDFS(node):",
        "  if node is null: return",
        "  visit(node)",
        "  treeDFS(node.left)",
        "  treeDFS(node.right)",
    ],
    "Graph BFS": [
        "function graphBFS(graph, start):",
        "  queue = [start]",
        "  visited = {start}",
        "  while queue is not empty:",
        "    node = queue.dequeue()",
        "    visit(node)",
        "    for neighbor in node.neighbors:",
        "      if neighbor not visited:",
        "        queue.enqueue(neighbor)",
    ],
    "Graph DFS": [
        "function graphDFS(node):",
        "  if node is visited: return",
        "  mark node as visited",
        "  visit(node)",
        "  for neighbor in node.neighbors:",
        "    if neighbor not visited:",
        "      graphDFS(neighbor)",
    ],
}


def render_pseudocode(algorithm_name: str, highlight_line: int):
    """
    Renders pseudo-code with the given line highlighted.
    highlight_line is 1-indexed (line 1 = first line of pseudo-code).
    """
    lines = PSEUDOCODE.get(algorithm_name)
    if not lines:
        st.caption("No pseudo-code available for this algorithm.")
        return

    html_parts = ['<div style="font-family: \'JetBrains Mono\', monospace; font-size: 0.82rem; line-height: 1.8;">']

    for i, line in enumerate(lines):
        line_num = i + 1
        # Escape HTML characters in pseudo-code
        escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        if line_num == highlight_line:
            html_parts.append(
                f'<div style="background: rgba(0, 210, 255, 0.15); '
                f'border-left: 3px solid #00d2ff; '
                f'padding: 2px 8px; border-radius: 4px; '
                f'color: #00d2ff; font-weight: 600;">'
                f'<span style="color: #6a6a80; width: 1.5em; display: inline-block;">{line_num}</span> '
                f'{escaped}</div>'
            )
        else:
            html_parts.append(
                f'<div style="padding: 2px 8px; color: #a0a0b8;">'
                f'<span style="color: #3a3a5c; width: 1.5em; display: inline-block;">{line_num}</span> '
                f'{escaped}</div>'
            )

    html_parts.append("</div>")

    st.markdown("".join(html_parts), unsafe_allow_html=True)
