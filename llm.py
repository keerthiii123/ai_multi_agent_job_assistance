import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE, override=True)


# ============================================================
# API KEY
# ============================================================

GEMINI_API_KEY = (
    os.getenv("GEMINI_API_KEY")
    or os.getenv("GOOGLE_API_KEY")
)

if not GEMINI_API_KEY:
    raise ValueError(
        "Gemini API key not found. "
        "Set GEMINI_API_KEY in Streamlit Cloud Secrets."
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# MODEL
# ============================================================

MODEL_NAME = "gemini-3.6-flash"


# ============================================================
# LLM FUNCTION
# ============================================================

def invoke_llm(prompt: str) -> str:

    if not prompt or not prompt.strip():
        return ""

    try:

        print("[Gemini] Calling model...")

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if response is None:
            return "LLM Error: Gemini returned an empty response."

        text = response.text

        if text:
            print("[Gemini] Response received successfully.")
            return text.strip()

        return "LLM Error: Gemini returned no text."

    except Exception as e:

        error_message = str(e)

        print("[Gemini] Error:")
        print(error_message)

        # Do NOT retry 429 quota errors.
        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:

            return (
                "LLM Error: Gemini API quota exceeded. "
                "Please try again after the quota resets."
            )

        return f"LLM Error: {error_message}"