<div align="center">

# 📊 DSA Visualizer + AI Explainer

**An interactive Data Structures & Algorithms visualizer with step-by-step execution, real-time pseudo-code highlighting, and AI-powered explanations.**

[![Python](https://img.shields.io/badge/Python-3.9+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini AI](https://img.shields.io/badge/Gemini_AI-2.5_Flash-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

[**Live Demo**](#-quick-start) · [**Features**](#-features) · [**Getting Started**](#-quick-start) · [**Contributing**](#-contributing)

</div>

---

## ✨ Features

### 🔢 Sorting Algorithms
| Algorithm | Technique | Time Complexity |
|-----------|-----------|-----------------|
| **Bubble Sort** | Compare adjacent elements, swap if out of order | O(n²) |
| **Merge Sort** | Divide and conquer with recursive merging | O(n log n) |
| **Quick Sort** | Partition around a pivot element | O(n log n) avg |
| **Insertion Sort** | Build sorted array one element at a time | O(n²) |
| **Selection Sort** | Find minimum and place at correct position | O(n²) |

### 🌳 Tree Traversals
- **BFS (Level Order)** — Visit nodes level by level using a queue
- **DFS (Preorder)** — Visit root → left → right recursively

### 🔗 Graph Traversals
- **BFS** — Explore neighbors first using a queue
- **DFS** — Explore as deep as possible before backtracking

### 🎨 Premium Dark UI
- Glassmorphism cards with backdrop blur
- Gradient accents & smooth micro-animations
- Custom typography (Inter + JetBrains Mono)
- Animated bar charts with glow effects for sorting
- Interactive tree and graph visualizations with node highlighting
- Step-by-step captions explaining each operation

### 📝 Live Pseudo-Code
- Real-time pseudo-code panel for every algorithm
- Current executing line is highlighted as you step through
- Supports all 9 algorithms (5 sorting + 2 tree + 2 graph)

### 🤖 AI Explainer (Gemini 2.5 Flash)
- One-click AI explanation for any algorithm run
- Explains how the algorithm works, step-by-step walkthrough, time complexity & real-life use case
- Rate-limited (10 calls/session) to preserve free API quota
- Prompt injection protection via input sanitization

### ▶️ Auto-Play Mode
- Auto-advance through steps with adjustable speed
- **Slow** (1s) / **Normal** (0.5s) / **Fast** (0.2s) playback
- Pause/resume at any time

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| [**Streamlit**](https://streamlit.io) | Web framework & interactive UI |
| [**Matplotlib**](https://matplotlib.org) | Chart rendering (bar, tree, graph) |
| [**Google GenAI**](https://ai.google.dev) | Gemini 2.5 Flash for AI explanations |
| [**Python 3.9+**](https://python.org) | Core language |

---

## 🚀 Quick Start

### Option 1 — GitHub Codespaces (Fastest)

Click the button below to launch instantly in your browser — no local setup needed:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/krish-the-goat/DSA-visualizer)

> The devcontainer auto-installs dependencies and starts the Streamlit server on port `8501`.

### Option 2 — Local Setup

#### 1. Clone the repository
```bash
git clone https://github.com/krish-the-goat/DSA-visualizer.git
cd DSA-visualizer
```

#### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Add your Gemini API key *(optional — app works without it)*
Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey), then:

```bash
# Option A: Environment variable
export GEMINI_API_KEY="your_api_key_here"

# Option B: Streamlit secrets
mkdir -p .streamlit
echo 'GEMINI_API_KEY = "your_api_key_here"' > .streamlit/secrets.toml
```

#### 5. Run the app
```bash
streamlit run app.py
```

The app will open at **http://localhost:8501** 🎉

---

## 📁 Project Structure

```
DSA-visualizer/
├── app.py                  # Main Streamlit application (routing, layout, state)
├── custom_theme.py         # Premium dark CSS theme with glassmorphism
├── security.py             # Input sanitization, rate limiting, prompt safety
├── requirements.txt        # Python dependencies
├── README.md
├── .gitignore
│
├── .streamlit/
│   ├── config.toml         # Streamlit server & theme configuration
│   └── secrets.toml        # API keys (gitignored)
│
├── .devcontainer/
│   └── devcontainer.json   # GitHub Codespaces / VS Code container config
│
├── algorithms/
│   ├── sorting.py          # Bubble, Merge, Quick, Insertion, Selection Sort
│   ├── trees.py            # Tree BFS (Level Order) & DFS (Preorder)
│   └── graphs.py           # Graph BFS & DFS with adjacency list input
│
├── visualizer/
│   ├── chart_utils.py      # Matplotlib chart rendering (bar, tree, graph)
│   └── pseudocode.py       # Pseudo-code display with live line highlighting
│
└── ai/
    └── explainer.py        # Gemini AI integration with rate limiting
```

---

## 🔒 Security

| Feature | Details |
|---------|---------|
| **Input Sanitization** | All user inputs validated via regex before processing |
| **Rate Limiting** | AI API calls capped at 10/session |
| **XSRF Protection** | Enabled via Streamlit server config |
| **Prompt Injection Guard** | User data escaped & truncated before AI prompts |
| **No Stack Traces** | Errors show user-friendly messages only |
| **Secrets Gitignored** | `.streamlit/secrets.toml` excluded from version control |
| **Array Size Limits** | Max 20 elements, values in [-9999, 9999] |
| **Graph Node Limits** | Max 15 nodes, alphanumeric labels only |

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**Made with ❤️ by [Krish](https://github.com/krish-the-goat)**

*Built with Streamlit + Gemini AI*

⭐ Star this repo if you found it useful!

</div>
