"""
Gemini API se algorithm ka ek complete explanation generate karta hai.
SIRF EK BAAR call hoti hai jab user button dabata hai.
"""

from google import genai
import streamlit as st

MODEL_NAME = "gemini-2.5-flash"


def _get_client():
    api_key = st.secrets.get("GEMINI_API_KEY", None)
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def explain_algorithm(algorithm_name, input_data, result):
    client = _get_client()
    if client is None:
        return "⚠️ Gemini API key set nahi hai. `.streamlit/secrets.toml` mein GEMINI_API_KEY daalo."

    prompt = f"""
Tum ek DSA teacher ho jo beginners ko Hinglish mein padhata hai.

Algorithm: {algorithm_name}
Input: {input_data}
Result/Output: {result}

Inhe explain karo:
1. Ye algorithm kaam kaise karta hai (2-3 lines mein, simple words)
2. Is specific input pe kya hua step-by-step (4-5 bullet points, short)
3. Is algorithm ki time complexity (ek line)
4. Kab use karte hain ye algorithm real life mein (ek example)

Hinglish mein likho (Hindi + English mix). Simple rakho, beginner ke liye.
Markdown use karo (bold, bullets). 150-200 words se zyada mat likho.
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"⚠️ AI explanation nahi mili ({type(e).__name__}). API key check karo ya baad mein try karo."
