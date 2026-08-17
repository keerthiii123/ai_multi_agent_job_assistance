import os
import re
from pypdf import PdfReader
from graph import build_graph
from report_generator import save_pdf, save_docx

# =====================================================
# CLEAN EXTRACTED PDF TEXT
# =====================================================

def clean_text(text: str) -> str:

    if not text:
        return ""

    # Join spaced letters
    text = re.sub(
        r'\b(?:[A-Za-z]\s+){2,}[A-Za-z]\b',
        lambda m: m.group(0).replace(" ", ""),
        text
    )

    # Split joined acronym + word
    text = re.sub(
        r'([A-Z]{2,})([A-Z]?[a-z])',
        r'\1 \2',
        text
    )

    # Common joined words
    text = text.replace("buildingGenerative", "building Generative")
    text = text.replace("inputand", "input and")

    # OCR fixes
    replacements = {

        "F ast API": "FastAPI",
        "F astAPI": "FastAPI",
        "Lang Chain": "LangChain",
        "Lang Graph": "LangGraph",
        "LangGr aph": "LangGraph",
        "Chroma DB": "ChromaDB",
        "Hugging Face": "HuggingFace",
        "Crew AI": "CrewAI",
        "Gr oq": "Groq",
        "Str eamlit": "Streamlit",
        "P ostgr eSQL": "PostgreSQL",
        "Ja v aScript": "JavaScript",
        "P ython": "Python",
        "P yth on": "Python",
        "R A G": "RAG",
        "L L M": "LLM",
        "REST f u l": "RESTful",
        "REST f u l API s": "RESTful APIs",
        "API s": "APIs",
        "Git h u b": "GitHub",
        "De v eloped": "Developed",
        "Integr ated": "Integrated",
        "inter activ e": "interactive"

    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =====================================================
# CLEAN RESUME
# =====================================================

def clean_resume_text(text: str):

    if not text:
        return ""

    return clean_text(text)


# =====================================================
# RESUME EXTRACTION
# =====================================================

def extract_resume_text(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Resume file not found: {file_path}"
        )

    extension = os.path.splitext(file_path)[1].lower()

    # PDF

    if extension == ".pdf":

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text() or ""

            text += page_text + "\n"

        return clean_resume_text(text)

    # DOCX

    elif extension == ".docx":

        from docx import Document

        document = Document(file_path)

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

        return clean_resume_text(text)

    # TXT

    elif extension == ".txt":

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return clean_resume_text(
                file.read()
            )

    else:

        raise ValueError(
            "Unsupported resume format. "
            "Use PDF, DOCX or TXT."
        )


# =====================================================
# MAIN
# =====================================================

def main():

    graph = build_graph()

    print("\n========================================")
    print("     AI MULTI-AGENT JOB ASSISTANT")
    print("========================================\n")

    user_query = input(
        "Enter your request: "
    )

    target_role = input(
        "Enter target role: "
    )

    resume_path = input(
        "Enter resume file path (PDF/DOCX/TXT): "
    )

    # Extract Resume

    try:

        resume_text = extract_resume_text(
            resume_path
        )

    except Exception as e:

        print("\n========================================")
        print("RESUME ERROR")
        print("========================================")

        print(f"\n{type(e).__name__}: {e}")

        return

    print("\nResume loaded successfully.")
    print(f"Extracted characters: {len(resume_text)}")

    job_description = input(
        "\nPaste job description (optional): "
    )

    # Initial State

    initial_state = {

        "user_query": user_query,

        "target_role": target_role,

        "resume_text": resume_text,

        "job_description": job_description,

        "plan": [],

        "resume_analysis": "",

        "skill_gap": "",

        "interview_questions": "",

        "job_match": "",

        "final_report": ""

    }

    # Run Graph

    try:

        result = graph.invoke(
            initial_state
        )

    except Exception as e:

        print("\n========================================")
        print("ERROR")
        print("========================================")

        print(f"\n{type(e).__name__}: {e}")

        return

    # Plan

    print("\n========================================")
    print("AGENT PLAN")
    print("========================================")

    print(result.get("plan", []))

    # Resume

    if result.get("resume_analysis"):

        print("\n========================================")
        print("RESUME ANALYSIS")
        print("========================================")

        print(result["resume_analysis"])

    # Skill Gap

    if result.get("skill_gap"):

        print("\n========================================")
        print("SKILL GAP ANALYSIS")
        print("========================================")

        print(result["skill_gap"])

    # Interview

    if result.get("interview_questions"):

        print("\n========================================")
        print("INTERVIEW QUESTIONS")
        print("========================================")

        print(result["interview_questions"])

    # Job Match

    if result.get("job_match"):

        print("\n========================================")
        print("JOB MATCH ANALYSIS")
        print("========================================")

        print(result["job_match"])

    # Final Report

    if result.get("final_report"):

        print("\n========================================")
        print("FINAL JOB READINESS REPORT")
        print("========================================")

        print(result["final_report"])

        try:

            pdf_file = save_pdf(
                result["final_report"]
            )

            docx_file = save_docx(
                result["final_report"]
            )

            print("\n========================================")
            print("REPORTS SAVED")
            print("========================================")

            print(f"PDF : {pdf_file}")
            print(f"DOCX: {docx_file}")

        except Exception as e:

            print("\nReport generation failed.")
            print(e)

    print("\n========================================")
    print("AGENT WORKFLOW COMPLETED")
    print("========================================")


# =====================================================
# RUN APPLICATION
# =====================================================

if __name__ == "__main__":
    main()