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
        f"API key not found.\n"
        f"Expected .env file at: {ENV_FILE}"
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

    if not prompt:
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

        return f"LLM Error: {error_message}"