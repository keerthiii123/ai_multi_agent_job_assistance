from state import AgentState
import re

# =====================================================
# IMPORTANT SKILLS
# =====================================================

IMPORTANT_SKILLS = [
    "python",
    "langchain",
    "langgraph",
    "rag",
    "chromadb",
    "fastapi",
    "streamlit",
    "huggingface",
    "embeddings",
    "groq",
    "git",
    "github"
]

# =====================================================
# NORMALIZE
# =====================================================

def normalize(text):

    if not text:
        return ""

    text = text.lower()
    text = text.replace("-", " ")
    text = text.replace("_", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()

# =====================================================
# SKILL CHECK
# =====================================================

def has_skill(text, skill):

    text = normalize(text)

    aliases = {
        "rag": ["rag", "retrieval augmented generation"],
        "fastapi": ["fastapi", "fast api"],
        "chromadb": ["chromadb", "chroma db"],
        "huggingface": [
            "huggingface",
            "hugging face",
            "sentence-transformers"
        ],
        "langgraph": ["langgraph", "lang graph"],
        "streamlit": ["streamlit"],
        "github": ["github"],
        "git": ["git"]
    }

    words = aliases.get(skill, [skill])

    for word in words:

        pattern = r"(?<!\w)" + re.escape(word) + r"(?!\w)"

        if re.search(pattern, text):
            return True

    return False

# =====================================================
# RESUME AGENT
# =====================================================

def resume_agent(state: AgentState):

    resume = state.get("resume_text", "")

    if not resume.strip():

        return {
            "resume_analysis":
            "Resume not found."
        }

    text = normalize(resume)

    strengths = []

    for skill in IMPORTANT_SKILLS:

        if has_skill(text, skill):

            strengths.append(skill.title())

    improvements = []

    # ----------------------------------------
    # Projects
    # ----------------------------------------

    if "project" not in text:

        improvements.append(
            "Add project descriptions."
        )

    # ----------------------------------------
    # Experience
    # ----------------------------------------

    if "experience" not in text:

        improvements.append(
            "Add work experience."
        )

    # ----------------------------------------
    # Education
    # ----------------------------------------

    if "education" not in text:

        improvements.append(
            "Clearly mention education."
        )

    # ----------------------------------------
    # Measurable achievements
    # ----------------------------------------

    numbers = re.findall(r"\d+", resume)

    if len(numbers) < 5:

        improvements.append(
            "Add measurable achievements."
        )

    # ----------------------------------------
    # Missing important skills
    # ----------------------------------------

    missing = []

    for skill in IMPORTANT_SKILLS:

        if not has_skill(text, skill):

            missing.append(skill.title())

    if missing:

        improvements.append(
            "Consider adding relevant skills only if you have used them: "
            + ", ".join(missing[:5])
        )

    # ----------------------------------------
    # Weakness
    # ----------------------------------------

    if improvements:

        weakness = (
            "Minor ATS improvements identified."
        )

    else:

        weakness = (
            "No major weaknesses detected."
        )

    # ----------------------------------------
    # Build Report
    # ----------------------------------------

    report = f"""
## Professional Summary

Candidate targeting the **AI Engineer** role with experience in Python and Generative AI technologies.

---

## Key Strengths

"""

    if strengths:

        for skill in strengths:

            report += f"✓ {skill}\n"

    else:

        report += "No major technical skills detected.\n"

    report += f"""

---

## Weaknesses

{weakness}

---

## Resume Improvement Suggestions

"""

    if improvements:

        for i, item in enumerate(
            improvements,
            start=1
        ):

            report += f"{i}. {item}\n"

    else:

        report += (
            "Your resume is well optimized.\n"
        )

    return {
        "resume_analysis": report
    }