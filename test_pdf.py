import re

# =====================================================
# CLEAN PDF TEXT
# =====================================================

def clean_text(text: str) -> str:
    if not text:
        return ""

    # Join words where every character is separated
    # Example: P y t h o n -> Python
    text = re.sub(
        r'\b(?:[A-Za-z]\s+){2,}[A-Za-z]\b',
        lambda m: m.group(0).replace(" ", ""),
        text
    )

    # Fix partially broken words
    replacements = {
        "Fast API": "FastAPI",
        "F ast API": "FastAPI",
        "F astAPI": "FastAPI",
        "Lang Chain": "LangChain",
        "Lang Graph": "LangGraph",
        "LangGr aph": "LangGraph",
        "Chroma DB": "ChromaDB",
        "Hugging Face": "HuggingFace",
        "Hugging F ace": "HuggingFace",
        "Crew AI": "CrewAI",
        "Gr oq": "Groq",
        "Str eamlit": "Streamlit",
        "P ostgr eSQL": "PostgreSQL",
        "Ja v aScript": "JavaScript",
        "P ython": "Python",
        "P yth on": "Python",
        "R A G": "RAG",
        "L L M": "LLM",
        "Git h u b": "GitHub",
        "REST f u l": "RESTful",
        "REST f u l API s": "RESTful APIs",
        "API s": "APIs",
        "De v eloped": "Developed",
        "Integr ated": "Integrated",
        "inter activ e": "interactive",
        "Pr ogr amming": "Programming",
        "Fr ameworks": "Frameworks",
        "Databases": "Databases"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()