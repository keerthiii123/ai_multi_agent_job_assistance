import os
import time
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

    max_retries = 3

    for attempt in range(max_retries):

        try:

            print(
                f"\n[Gemini] Calling model "
                f"(attempt {attempt + 1}/{max_retries})..."
            )

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            if response is None:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            text = response.text

            if text:
                print("[Gemini] Response received successfully.")
                return text.strip()

            raise RuntimeError(
                "Gemini returned no text."
            )

        except Exception as e:

            print(
                f"\n[Gemini] Attempt {attempt + 1} failed:"
            )
            print(str(e))

            if attempt < max_retries - 1:

                wait_time = 2 ** attempt

                print(
                    f"[Gemini] Retrying in "
                    f"{wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:

                print(
                    "\n[Gemini] All retry attempts failed."
                )

                return f"LLM Error: {str(e)}"