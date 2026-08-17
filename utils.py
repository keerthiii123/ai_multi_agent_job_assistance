import re
from pypdf import PdfReader


# =====================================================
# PDF TEXT EXTRACTION
# =====================================================

def extract_pdf_text(file_path):

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:

        text = page.extract_text() or ""

        pages.append(text)

    text = "\n".join(pages)

    return clean_extracted_text(text)


# =====================================================
# CLEAN PDF TEXT
# =====================================================

def clean_extracted_text(text):

    if not text:
        return ""

    # ---------------------------------------------
    # Fix character-spaced PDF extraction
    #
    # P y t h o n -> Python
    # L a n g C h a i n -> LangChain
    # R A G -> RAG
    # ---------------------------------------------

    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Fix spaces between individual characters
        line = re.sub(
            r'(?<!\w)([A-Za-z])(?:\s+([A-Za-z])){2,}(?!\w)',
            lambda match: match.group(0).replace(" ", ""),
            line
        )

        cleaned_lines.append(line)

    text = "\n".join(cleaned_lines)

    # ---------------------------------------------
    # Fix common PDF spacing problems
    # ---------------------------------------------

    replacements = {

        "F ast API": "FastAPI",
        "F astapi": "FastAPI",

        "P ython": "Python",
        "P y t h o n": "Python",

        "L angChain": "LangChain",
        "L a n g C h a i n": "LangChain",

        "L angGraph": "LangGraph",
        "L a n g G r a p h": "LangGraph",

        "C hromaDB": "ChromaDB",
        "C h r o m a D B": "ChromaDB",

        "S treamlit": "Streamlit",
        "S t r e a m l i t": "Streamlit",

        "Hugging F ace": "HuggingFace",
        "H u g g i n g F a c e": "HuggingFace",

        "G roq": "Groq",
        "G r o q": "Groq",

        "G it": "Git",
        "G i t": "Git",

        "G itHub": "GitHub",
        "G i t H u b": "GitHub",

        "D jango": "Django",

        "P ostgreSQL": "PostgreSQL",
        "M ySQL": "MySQL",

        "R A G": "RAG",

        "L L M": "LLM",

        "G enerative A I": "Generative AI",

        "C rew A I": "CrewAI",

        "R E S T": "REST",

        "A P I": "API",

        "J S": "JS",
    }

    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )

    # ---------------------------------------------
    # Fix excessive spaces
    # ---------------------------------------------

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()