import streamlit as st
import tempfile
import re
from pypdf import PdfReader

from graph import build_graph
from report_generator import save_pdf, save_docx

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Multi-Agent Job Assistant",
    page_icon="🤖",
    layout="wide"
)

# ==========================================
# TEXT CLEANING
# ==========================================

def clean_text(text: str):

    if not text:
        return ""

    text = re.sub(
        r"\b(?:[A-Za-z]\s+){2,}[A-Za-z]\b",
        lambda m: m.group(0).replace(" ", ""),
        text
    )

    text = re.sub(
        r"\b([A-Z]{2,})([A-Z]?[a-z])",
        r"\1 \2",
        text
    )

    replacements = {
        "LangGr aph": "LangGraph",
        "Lang Graph": "LangGraph",
        "R A G": "RAG",
        "Hugging F ace": "HuggingFace",
        "F ast API": "FastAPI",
        "Chroma DB": "ChromaDB",
        "Crew AI": "CrewAI",
        "Gr oq": "Groq",
        "Str eamlit": "Streamlit",
        "P ostgr eSQL": "PostgreSQL",
        "Ja v aScript": "JavaScript",
        "P ython": "Python",
        "P yth on": "Python",
        "REST f u l": "RESTful",
        "API s": "APIs",
        "Git h u b": "GitHub",
        "De v eloped": "Developed",
        "Integr ated": "Integrated",
        "inter activ e": "interactive",
        "buildingGenerative": "building Generative",
        "inputand": "input and"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"\s+", " ", text)

    return text.strip()

# ==========================================
# PDF EXTRACTION
# ==========================================

def extract_resume(uploaded_file):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        path = tmp.name

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return clean_text(text)

# ==========================================
# HEADER
# ==========================================

st.title("🤖 AI Multi-Agent Job Assistant")
st.caption("Resume Analysis • Resume Rewrite • Skill Gap • Job Match • Interview Questions")

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("Configuration")

    target_role = st.selectbox(
        "Target Role",
        [
            "AI Engineer",
            "Python Developer",
            "Full Stack Developer",
            "Data Analyst",
            "Software Engineer"
        ]
    )

    difficulty = st.selectbox(
        "Interview Difficulty",
        ["Easy", "Medium", "Hard"],
        index=1
    )

    user_query = st.text_input(
        "Request",
        "Analyze my resume and prepare interview questions"
    )

# ==========================================
# INPUTS
# ==========================================

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description (Optional)",
    height=180
)

# ==========================================
# RUN BUTTON
# ==========================================

if st.button("🚀 Analyze Resume", use_container_width=True):

    if uploaded_file is None:
        st.error("Please upload a resume.")
        st.stop()

    try:

        progress = st.progress(0)
        status = st.empty()

        status.text("📄 Reading Resume...")
        resume_text = extract_resume(uploaded_file)
        progress.progress(25)

        status.text("🤖 Running AI Multi-Agent Workflow...")
        graph = build_graph()

        state = {
            "user_query": user_query,
            "target_role": target_role,
            "resume_text": resume_text,
            "job_description": job_description,
            "plan": [],
            "resume_analysis": "",
            "resume_rewrite": "",
            "skill_gap": "",
            "job_match": "",
            "interview_questions": "",
            "final_report": ""
        }

        result = graph.invoke(state)

        progress.progress(100)
        status.success("✅ Analysis Completed!")

    except Exception as e:
        st.error(f"Error: {e}")
        st.stop()

    # ==========================================
    # DASHBOARD METRICS
    # ==========================================

    ats = re.search(
        r"ATS Match Score.*?(\d+)",
        result.get("job_match", ""),
        re.S
    )

    skill = re.search(
        r"Overall Role Skill Match.*?(\d+)%",
        result.get("skill_gap", ""),
        re.S
    )

    jd = re.search(
        r"Job Description Skill Match.*?(\d+)%",
        result.get("skill_gap", ""),
        re.S
    )

    missing = re.search(
        r"Skills missing:\s*\*\*(\d+)\*\*",
        result.get("skill_gap", ""),
        re.S
    )

    st.divider()
    st.subheader("📊 Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("ATS Score", f"{ats.group(1) if ats else '--'}%")
    c2.metric("Skill Match", f"{skill.group(1) if skill else '--'}%")
    c3.metric("JD Match", f"{jd.group(1) if jd else '--'}%")
    c4.metric("Missing Skills", missing.group(1) if missing else "--")

    st.divider()

    # ==========================================
    # AGENT PLAN
    # ==========================================

    with st.expander("🧠 Agent Plan"):
        st.json(result.get("plan", []))

    # ==========================================
    # TABS
    # ==========================================

    tabs = st.tabs([
        "📄 Resume Analysis",
        "✨ Resume Rewrite",
        "🎯 Skill Gap",
        "📊 Job Match",
        "💬 Interview",
        "📘 Final Report"
    ])

    with tabs[0]:
        st.markdown(result.get("resume_analysis", "No analysis available."))

    with tabs[1]:
        st.markdown(result.get("resume_rewrite", "No rewritten resume generated."))

    with tabs[2]:
        st.markdown(result.get("skill_gap", "No skill gap analysis available."))

    with tabs[3]:
        st.markdown(result.get("job_match", "No job match analysis available."))

    with tabs[4]:
        st.markdown(result.get("interview_questions", "No interview questions generated."))

    with tabs[5]:

        st.markdown(result.get("final_report", "No final report generated."))

        if result.get("final_report"):

            pdf_path = save_pdf(result["final_report"])
            docx_path = save_docx(result["final_report"])

            col1, col2 = st.columns(2)

            with col1:
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "⬇️ Download PDF",
                        f,
                        file_name="job_readiness_report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

            with col2:
                with open(docx_path, "rb") as f:
                    st.download_button(
                        "⬇️ Download DOCX",
                        f,
                        file_name="job_readiness_report.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")
st.caption("Built with ❤️ using Streamlit • LangGraph • Gemini • Python")