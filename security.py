"""
Security module — input sanitization, rate limiting, and security constants.
All user-facing inputs must be validated through these functions before processing.
"""

import re
import streamlit as st

# ─── Security Constants ───────────────────────────────────────────────────────

MAX_ARRAY_SIZE = 20
MAX_ARRAY_VALUE = 9999
MIN_ARRAY_VALUE = -9999
MAX_GRAPH_NODES = 15
MAX_NODE_LABEL_LENGTH = 10
MAX_AI_CALLS_PER_SESSION = 10
AI_PROMPT_MAX_LENGTH = 2000
ALLOWED_NODE_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")


# ─── Input Sanitization ──────────────────────────────────────────────────────

def sanitize_array_input(raw_text: str) -> list[int]:
    """
    Validates and parses a comma-separated string of integers.
    Raises ValueError with a user-safe message on invalid input.
    """
    if not raw_text or not raw_text.strip():
        raise ValueError("Please enter an array of numbers.")

    # Strip and reject any characters that aren't digits, commas, spaces, or minus signs
    cleaned = raw_text.strip()
    if re.search(r"[^0-9,\s\-]", cleaned):
        raise ValueError(
            "Invalid characters detected. Use only numbers separated by commas. "
            "Example: 5, 2, 8, 1, 9"
        )

    parts = [p.strip() for p in cleaned.split(",") if p.strip()]

    if len(parts) < 2:
        raise ValueError("Enter at least 2 numbers.")

    if len(parts) > MAX_ARRAY_SIZE:
        raise ValueError(f"Maximum {MAX_ARRAY_SIZE} numbers allowed.")

    result = []
    for part in parts:
        try:
            val = int(part)
        except ValueError:
            raise ValueError(
                f"'{part}' is not a valid integer. Use only whole numbers."
            )

        if val < MIN_ARRAY_VALUE or val > MAX_ARRAY_VALUE:
            raise ValueError(
                f"Value {val} is out of range. "
                f"Allowed range: {MIN_ARRAY_VALUE} to {MAX_ARRAY_VALUE}."
            )
        result.append(val)

    return result


def sanitize_tree_input(raw_text: str) -> list[int]:
    """
    Validates and parses tree node values (level-order).
    Same rules as array input but allows single element.
    """
    if not raw_text or not raw_text.strip():
        raise ValueError("Please enter tree node values.")

    cleaned = raw_text.strip()
    if re.search(r"[^0-9,\s\-]", cleaned):
        raise ValueError(
            "Invalid characters detected. Use only numbers separated by commas."
        )

    parts = [p.strip() for p in cleaned.split(",") if p.strip()]

    if len(parts) == 0:
        raise ValueError("Enter at least 1 value.")

    if len(parts) > MAX_ARRAY_SIZE:
        raise ValueError(f"Maximum {MAX_ARRAY_SIZE} values allowed.")

    result = []
    for part in parts:
        try:
            val = int(part)
        except ValueError:
            raise ValueError(f"'{part}' is not a valid integer.")

        if val < MIN_ARRAY_VALUE or val > MAX_ARRAY_VALUE:
            raise ValueError(
                f"Value {val} is out of range ({MIN_ARRAY_VALUE} to {MAX_ARRAY_VALUE})."
            )
        result.append(val)

    return result


def sanitize_node_label(raw_text: str) -> str:
    """
    Validates a single graph node label.
    Only alphanumeric characters and underscores allowed.
    """
    label = raw_text.strip()
    if not label:
        raise ValueError("Node label cannot be empty.")

    if len(label) > MAX_NODE_LABEL_LENGTH:
        raise ValueError(
            f"Node label too long (max {MAX_NODE_LABEL_LENGTH} characters)."
        )

    if not ALLOWED_NODE_PATTERN.match(label):
        raise ValueError(
            f"Invalid node label '{label}'. "
            "Only letters, numbers, and underscores are allowed."
        )

    return label


def sanitize_graph_input(raw_text: str) -> dict:
    """
    Validates and parses graph adjacency list from text.
    Format per line: 'NodeLabel: Neighbor1, Neighbor2'
    Returns a validated adjacency dict.
    """
    if not raw_text or not raw_text.strip():
        raise ValueError("Please define a graph.")

    lines = raw_text.strip().split("\n")
    graph = {}

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue

        if ":" not in line:
            raise ValueError(
                f"Line {line_num}: Invalid format. "
                "Use 'Node: Neighbor1, Neighbor2'. Example: 'A: B, C'"
            )

        node_part, neighbors_part = line.split(":", 1)
        node = sanitize_node_label(node_part)

        neighbors = []
        for n in neighbors_part.split(","):
            n = n.strip()
            if n:
                neighbors.append(sanitize_node_label(n))

        if len(graph) >= MAX_GRAPH_NODES and node not in graph:
            raise ValueError(f"Maximum {MAX_GRAPH_NODES} nodes allowed.")

        graph[node] = neighbors

    if not graph:
        raise ValueError("Graph is empty. Define at least one node with neighbors.")

    return graph


# ─── Rate Limiting ────────────────────────────────────────────────────────────

def check_ai_rate_limit() -> bool:
    """
    Returns True if AI call is allowed, False if rate limit exceeded.
    Tracks calls in session state.
    """
    if "ai_call_count" not in st.session_state:
        st.session_state.ai_call_count = 0

    return st.session_state.ai_call_count < MAX_AI_CALLS_PER_SESSION


def increment_ai_call_count():
    """Increments the AI call counter after a successful call."""
    if "ai_call_count" not in st.session_state:
        st.session_state.ai_call_count = 0
    st.session_state.ai_call_count += 1


def get_ai_calls_remaining() -> int:
    """Returns the number of AI calls remaining in this session."""
    used = st.session_state.get("ai_call_count", 0)
    return max(0, MAX_AI_CALLS_PER_SESSION - used)


# ─── Utility ──────────────────────────────────────────────────────────────────

def escape_for_prompt(text: str) -> str:
    """
    Escapes user-provided data before inserting into an AI prompt.
    Prevents prompt injection by stripping control characters and
    limiting length.
    """
    if not isinstance(text, str):
        text = str(text)

    # Remove control characters except newlines and tabs
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

    # Truncate to prevent excessively long prompts
    if len(text) > AI_PROMPT_MAX_LENGTH:
        text = text[:AI_PROMPT_MAX_LENGTH] + "... (truncated)"

    return text
