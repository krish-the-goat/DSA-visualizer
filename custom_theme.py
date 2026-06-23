"""
Custom CSS theme injection for Streamlit.
Provides a premium dark theme with glassmorphism, gradients,
smooth animations, and custom typography.
"""

import streamlit as st


def inject_custom_css():
    """Injects the full custom CSS theme into the Streamlit app."""
    st.markdown(
        """
        <style>
        /* ─── Google Font Import ──────────────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        /* ─── Root Variables ──────────────────────────────────────── */
        :root {
            --bg-primary: #0f0f1a;
            --bg-secondary: #1a1a2e;
            --bg-card: rgba(30, 30, 50, 0.6);
            --bg-card-hover: rgba(40, 40, 65, 0.7);
            --text-primary: #e8e8f0;
            --text-secondary: #a0a0b8;
            --text-muted: #6a6a80;
            --accent-cyan: #00d2ff;
            --accent-purple: #7b68ee;
            --accent-pink: #ff6b9d;
            --accent-green: #4ade80;
            --accent-orange: #ffa552;
            --gradient-main: linear-gradient(135deg, #00d2ff, #7b68ee);
            --gradient-warm: linear-gradient(135deg, #ff6b9d, #ffa552);
            --gradient-success: linear-gradient(135deg, #4ade80, #00d2ff);
            --glass-border: rgba(255, 255, 255, 0.08);
            --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* ─── Global Styles ───────────────────────────────────────── */
        .stApp {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }

        /* Main container background */
        .stApp > header {
            background: transparent !important;
        }

        /* ─── Typography ──────────────────────────────────────────── */
        h1 {
            background: var(--gradient-main);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 700 !important;
            font-size: 2.2rem !important;
            letter-spacing: -0.02em;
            padding-bottom: 0.5rem;
        }

        h2, h3 {
            color: var(--text-primary) !important;
            font-weight: 600 !important;
        }

        p, span, label, .stMarkdown {
            font-family: 'Inter', sans-serif !important;
        }

        /* ─── Sidebar ─────────────────────────────────────────────── */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #12122a 0%, #1a1a35 100%) !important;
            border-right: 1px solid var(--glass-border) !important;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2 {
            -webkit-text-fill-color: var(--text-primary) !important;
            background: none !important;
        }

        /* ─── Cards / Containers ──────────────────────────────────── */
        div[data-testid="stExpander"],
        .stTabs [data-baseweb="tab-panel"] {
            background: var(--bg-card) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 16px !important;
            padding: 1rem !important;
            box-shadow: var(--glass-shadow) !important;
        }

        /* ─── Buttons ─────────────────────────────────────────────── */
        .stButton > button {
            font-family: 'Inter', sans-serif !important;
            font-weight: 500 !important;
            border-radius: 12px !important;
            padding: 0.5rem 1.5rem !important;
            border: 1px solid var(--glass-border) !important;
            background: var(--bg-card) !important;
            color: var(--text-primary) !important;
            backdrop-filter: blur(8px) !important;
            transition: var(--transition-smooth) !important;
            letter-spacing: 0.01em;
        }

        .stButton > button:hover {
            background: var(--bg-card-hover) !important;
            border-color: var(--accent-cyan) !important;
            box-shadow: 0 0 20px rgba(0, 210, 255, 0.15) !important;
            transform: translateY(-1px);
        }

        /* Primary buttons */
        .stButton > button[kind="primary"],
        .stButton > button[data-testid="stBaseButton-primary"] {
            background: var(--gradient-main) !important;
            border: none !important;
            color: #fff !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 15px rgba(0, 210, 255, 0.3) !important;
        }

        .stButton > button[kind="primary"]:hover,
        .stButton > button[data-testid="stBaseButton-primary"]:hover {
            box-shadow: 0 6px 25px rgba(0, 210, 255, 0.45) !important;
            transform: translateY(-2px);
        }

        /* Disabled buttons */
        .stButton > button:disabled {
            opacity: 0.4 !important;
            transform: none !important;
            box-shadow: none !important;
        }

        /* ─── Input Fields ────────────────────────────────────────── */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            font-family: 'JetBrains Mono', monospace !important;
            background: rgba(15, 15, 30, 0.8) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 12px !important;
            color: var(--text-primary) !important;
            transition: var(--transition-smooth) !important;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: var(--accent-cyan) !important;
            box-shadow: 0 0 15px rgba(0, 210, 255, 0.1) !important;
        }

        /* ─── Select Box ──────────────────────────────────────────── */
        .stSelectbox > div > div {
            background: rgba(15, 15, 30, 0.8) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 12px !important;
        }

        /* ─── Radio Buttons ───────────────────────────────────────── */
        .stRadio > div {
            gap: 0.5rem;
        }

        .stRadio > div > label {
            background: var(--bg-card) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 12px !important;
            padding: 0.6rem 1.2rem !important;
            transition: var(--transition-smooth) !important;
        }

        .stRadio > div > label:hover {
            border-color: var(--accent-purple) !important;
            background: var(--bg-card-hover) !important;
        }

        /* ─── Tabs ────────────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: transparent !important;
        }

        .stTabs [data-baseweb="tab"] {
            font-family: 'Inter', sans-serif !important;
            font-weight: 500 !important;
            border-radius: 10px !important;
            padding: 0.5rem 1rem !important;
            background: var(--bg-card) !important;
            border: 1px solid var(--glass-border) !important;
            color: var(--text-secondary) !important;
            transition: var(--transition-smooth) !important;
        }

        .stTabs [data-baseweb="tab"]:hover {
            color: var(--text-primary) !important;
            border-color: var(--accent-purple) !important;
        }

        .stTabs [aria-selected="true"] {
            background: var(--gradient-main) !important;
            color: #fff !important;
            border: none !important;
        }

        .stTabs [data-baseweb="tab-highlight"] {
            display: none !important;
        }

        .stTabs [data-baseweb="tab-border"] {
            display: none !important;
        }

        /* ─── Divider ─────────────────────────────────────────────── */
        hr {
            border-color: var(--glass-border) !important;
            margin: 1.5rem 0 !important;
        }

        /* ─── Info / Warning / Error boxes ────────────────────────── */
        .stAlert {
            background: var(--bg-card) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 12px !important;
            backdrop-filter: blur(8px) !important;
        }

        /* ─── Checkbox ────────────────────────────────────────────── */
        .stCheckbox label span {
            color: var(--text-primary) !important;
        }

        /* ─── Slider ──────────────────────────────────────────────── */
        .stSlider > div > div > div > div {
            background: var(--gradient-main) !important;
        }

        /* ─── Caption ─────────────────────────────────────────────── */
        .stCaption, small {
            color: var(--text-muted) !important;
        }

        /* ─── Step Caption Card ───────────────────────────────────── */
        .step-caption {
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: 14px;
            padding: 1rem 1.2rem;
            margin: 0.8rem 0;
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            color: var(--text-primary);
            box-shadow: var(--glass-shadow);
            line-height: 1.5;
        }

        .step-caption .step-icon {
            font-size: 1.2rem;
            margin-right: 0.5rem;
        }

        /* ─── Navigation Bar ──────────────────────────────────────── */
        .nav-container {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin: 0.5rem 0;
        }

        /* ─── Progress Bar (Step Counter) ─────────────────────────── */
        .step-progress {
            background: rgba(30, 30, 50, 0.6);
            border-radius: 20px;
            padding: 0.3rem 1rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: var(--text-secondary);
            border: 1px solid var(--glass-border);
        }

        /* ─── AI Explanation Card ─────────────────────────────────── */
        .ai-card {
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: 14px;
            padding: 1.2rem;
            box-shadow: var(--glass-shadow);
            color: var(--text-primary);
            line-height: 1.6;
        }

        .ai-card h4 {
            background: var(--gradient-main);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.8rem;
        }

        /* ─── Rate Limit Badge ────────────────────────────────────── */
        .rate-badge {
            display: inline-block;
            background: rgba(74, 222, 128, 0.15);
            color: var(--accent-green);
            padding: 0.2rem 0.6rem;
            border-radius: 8px;
            font-size: 0.75rem;
            font-family: 'JetBrains Mono', monospace;
            border: 1px solid rgba(74, 222, 128, 0.2);
        }

        /* ─── Animations ──────────────────────────────────────────── */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        .animate-fade {
            animation: fadeIn 0.4s ease-out;
        }

        .animate-pulse {
            animation: pulse 1.5s ease-in-out infinite;
        }

        /* ─── Scrollbar ───────────────────────────────────────────── */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }

        ::-webkit-scrollbar-track {
            background: var(--bg-primary);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--text-muted);
            border-radius: 3px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--text-secondary);
        }

        /* ─── Hide Streamlit Branding ─────────────────────────────── */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] {
            background: transparent !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
