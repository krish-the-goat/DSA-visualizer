# 📊 DSA Visualizer + AI Explainer

A web app that brings DSA to life — watch sorting algorithms animate in real time, explore trees and graphs step by step, and get AI-powered explanations that actually make sense.

🔗 **Live Demo:** [dsa-visualizer-7gxjaptnabn8ngsom4qvth.streamlit.app](https://dsa-visualizer-7gxjaptnabn8ngsom4qvth.streamlit.app/)

---

## ✨ Features

- **Sorting Visualizer** — Watch Bubble Sort, Merge Sort, and Quick Sort animate as bar charts
- **Tree Traversal** — Visualize BFS (Level Order) and DFS (Preorder) on a Binary Tree
- **Graph Traversal** — Build your own graph and watch BFS/DFS explore it node by node
- **Manual Step Control** — Go at your own pace with Next/Previous buttons
- **AI Explainer** — Gemini AI gives you one clean, beginner-friendly explanation per run (not per step — no rate limit issues)
- **Edge Case Handling** — Invalid input, empty arrays, oversized inputs — all handled gracefully

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web app framework |
| Matplotlib | Algorithm animations |
| Google Gemini API | AI-powered explanations |
| Streamlit Cloud | Deployment |

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/dsa-visualizer.git
cd dsa-visualizer
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your Gemini API key

Create a `.streamlit/secrets.toml` file:
```toml
GEMINI_API_KEY = "your-api-key-here"
```

> ⚠️ This file is already in `.gitignore` — it won't accidentally get pushed to GitHub.

### 4. Run the app
```bash
streamlit run app.py
```

Opens at `http://localhost:8501` in your browser.

---

## 📁 Project Structure

```
dsa-visualizer/
├── app.py                    # Main Streamlit app (entry point)
├── requirements.txt          # Project dependencies
├── .gitignore                # Excludes secrets and cache files
│
├── algorithms/
│   ├── sorting.py            # Bubble, Merge, Quick Sort
│   ├── trees.py              # Binary Tree BFS/DFS
│   └── graphs.py             # Graph BFS/DFS
│
├── visualizer/
│   └── chart_utils.py        # Matplotlib chart rendering
│
└── ai/
    └── explainer.py          # Gemini API integration
```

---

## 🧠 DSA Concepts Covered

**Sorting**
- Bubble Sort — O(n²), simple comparison-based swapping
- Merge Sort — O(n log n), divide and conquer
- Quick Sort — O(n log n) average, pivot-based partitioning

**Trees**
- BFS (Level Order) — Queue-based level-by-level traversal
- DFS (Preorder) — Recursive root → left → right traversal

**Graphs**
- BFS — Queue-based, great for shortest path problems
- DFS — Recursive, great for cycle detection and pathfinding

---

## 💡 How It Works

1. **Algorithm logic** lives in `algorithms/` — pure Python, completely independent of the UI
2. Every algorithm returns a **list of steps** — each step captures the exact state of the array/tree/graph at that moment
3. The **visualizer** renders each step one at a time using Matplotlib
4. The **AI explainer** is called exactly once per run (on button click) — no per-step API calls, no rate limiting

---

## 📚 What I Built and Learned

- Sorting algorithm internals — Bubble, Merge, Quick Sort
- Tree traversal — BFS, DFS, and how to maintain consistent node IDs across functions
- Graph representation using adjacency lists, with proper cycle handling
- Streamlit — session state management, layout, secrets
- Matplotlib — dynamic chart rendering for different data structures
- LLM API integration — using Gemini as a feature inside an app
- Modular code architecture — keeping UI, logic, and AI completely separate
- Deployment — live app on Streamlit Cloud

---

