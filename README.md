# 📊 DSA Visualizer + AI Explainer

A premium, interactive Data Structures & Algorithms visualizer built with Streamlit. Step through sorting algorithms, tree traversals, and graph traversals with real-time visualizations, pseudo-code highlighting, and AI-powered explanations.

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red?style=flat-square&logo=streamlit)
![Gemini AI](https://img.shields.io/badge/Gemini_AI-2.5_Flash-purple?style=flat-square&logo=google)

---

## ✨ Features

### 🔢 Sorting Algorithms
- **Bubble Sort** — Compare adjacent elements, swap if out of order
- **Merge Sort** — Divide and conquer with recursive merging
- **Quick Sort** — Partition around a pivot element
- **Insertion Sort** — Build sorted array one element at a time
- **Selection Sort** — Find minimum and place at correct position

### 🌳 Tree Traversals
- **BFS (Level Order)** — Visit nodes level by level using a queue
- **DFS (Preorder)** — Visit root → left → right recursively

### 🔗 Graph Traversals
- **BFS** — Explore neighbors first using a queue
- **DFS** — Explore as deep as possible before backtracking

### 🎨 Premium UI
- Dark theme with glassmorphism and gradient accents
- Animated chart visualizations with glow effects
- Step-by-step captions explaining each operation
- Pseudo-code panel with live line highlighting

### 🤖 AI Explainer (Gemini)
- One-click AI explanation for any algorithm run
- Powered by Google Gemini 2.5 Flash
- Rate-limited to preserve free API quota

### ▶️ Auto-Play
- Auto-advance through steps with adjustable speed
- Slow / Normal / Fast playback modes
- Pause/resume at any time

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web framework and UI |
| **Matplotlib** | Chart and graph rendering |
| **Google Gemini AI** | Algorithm explanations |
| **Python 3.9+** | Core language |

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/dsa-visualizer.git
cd dsa-visualizer
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Gemini API key
Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey), then edit `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your_actual_api_key_here"
```

Or set it as an environment variable:
```bash
export GEMINI_API_KEY="your_actual_api_key_here"
```

### 5. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 📁 Project Structure

```
dsa-visualizer/
├── app.py                  # Main Streamlit application
├── custom_theme.py         # Premium dark theme CSS injection
├── security.py             # Input sanitization & rate limiting
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── .gitignore              # Git ignore rules
├── .streamlit/
│   ├── config.toml         # Streamlit server configuration
│   └── secrets.toml        # API keys (gitignored)
├── algorithms/
│   ├── sorting.py          # Sorting algorithms (5 algorithms)
│   ├── trees.py            # Tree traversal algorithms
│   └── graphs.py           # Graph traversal algorithms
├── visualizer/
│   ├── chart_utils.py      # Matplotlib chart rendering
│   └── pseudocode.py       # Pseudo-code display with highlighting
└── ai/
    └── explainer.py        # Gemini AI integration
```

---

## 🔒 Security

- **Input sanitization**: All user inputs are validated and sanitized before processing
- **Rate limiting**: AI API calls are rate-limited per session
- **XSRF protection**: Enabled via Streamlit server config
- **CORS disabled**: Cross-origin requests are blocked
- **No stack trace leaks**: Errors show user-friendly messages only
- **Environment-based secrets**: API keys can be set via environment variables
- **Secrets gitignored**: `.streamlit/secrets.toml` is excluded from version control

---

## 📝 License

This project is open source. Feel free to use, modify, and distribute.

---

Made with ❤️ using Streamlit + Gemini AI
