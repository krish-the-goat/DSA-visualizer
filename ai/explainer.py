"""
AI Explainer — generates a single comprehensive explanation per algorithm run
using the Gemini API. Called ONCE when user clicks the run button.

Security: Uses environment variables for API key, sanitizes prompt inputs,
wraps all API calls with safe error handling (no stack traces leaked).
"""

import os
import streamlit as st
from google import genai
from security import escape_for_prompt, check_ai_rate_limit, increment_ai_call_count

MODEL_NAME = "gemini-2.5-flash"
API_TIMEOUT_SECONDS = 30


def _get_client():
    """
    Creates Gemini client using API key from environment or Streamlit secrets.
    Environment variable takes priority for production deployments.
    Returns None if no API key is configured.
    """
    api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        return None

    return genai.Client(api_key=api_key)


def explain_algorithm(algorithm_name: str, input_data, result) -> str:
    """
    Generates a single AI explanation for the given algorithm run.
    Returns a formatted explanation string, or a safe error message.
    """
    # Rate limit check
    if not check_ai_rate_limit():
        return (
            "⚠️ AI explanation limit reached for this session. "
            "Restart the app to reset the counter."
        )

    client = _get_client()
    if client is None:
        return (
            "⚠️ Gemini API key not configured. "
            "Add your key to `.streamlit/secrets.toml` or set the "
            "GEMINI_API_KEY environment variable."
        )

    # Sanitize all user-provided data before inserting into prompt
    safe_algo = escape_for_prompt(str(algorithm_name))
    safe_input = escape_for_prompt(str(input_data))
    safe_result = escape_for_prompt(str(result))

    prompt = f"""You are a DSA teacher explaining algorithms to beginners.

Algorithm: {safe_algo}
Input: {safe_input}
Result/Output: {safe_result}

Please explain:
1. How this algorithm works (2-3 lines, simple words)
2. What happened on this specific input, step-by-step (4-5 bullet points, short)
3. Time complexity of this algorithm (one line)
4. A real-life example of when this algorithm is useful (one example)

Write in clear, simple English. Use Markdown formatting (bold, bullets).
Keep it under 200 words.
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        increment_ai_call_count()
        return response.text.strip()

    except Exception:
        # Never leak internal error details to the user
        return (
            "⚠️ Could not generate AI explanation. "
            "Please check your API key and try again later."
        )
