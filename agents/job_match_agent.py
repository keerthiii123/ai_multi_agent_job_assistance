from state import AgentState
from agents.skill_agent import ROLE_SKILLS, find_skills, normalize

# ==========================================
# JOB MATCH AGENT
# ==========================================

def job_match_agent(state: AgentState):

    resume_text = normalize(state.get("resume_text", ""))
    job_description = normalize(state.get("job_description", ""))
    target_role = state.get("target_role", "AI Engineer")

    role_skills = ROLE_SKILLS.get(target_role)

    if not role_skills:
        return {
            "job_match": f"No skill mapping available for {target_role}."
        }

    # ==========================================
    # FIND MATCHES
    # ==========================================

    matched_skills = find_skills(resume_text, role_skills)

    # JD-based matching if JD exists
    if job_description.strip():
        jd_skills = find_skills(job_description, role_skills)
    else:
        jd_skills = role_skills

    missing_skills = [
        skill for skill in jd_skills
        if skill not in matched_skills
    ]

    total = len(jd_skills)
    matched = len(jd_skills) - len(missing_skills)

    ats_score = round((matched / total) * 100) if total else 0

    # ==========================================
    # RECOMMENDATION
    # ==========================================

    if ats_score >= 90:
        recommendation = "🟢 Excellent Match"

    elif ats_score >= 75:
        recommendation = "🟡 Good Match"

    else:
        recommendation = "🔴 Needs Improvement"

    # ==========================================
    # STRENGTHS
    # ==========================================

    strengths = []

    if "python" in matched_skills:
        strengths.append("Strong Python foundation.")

    if "langchain" in matched_skills:
        strengths.append("Hands-on LangChain experience.")

    if "rag" in matched_skills:
        strengths.append("Practical RAG implementation.")

    if "streamlit" in matched_skills:
        strengths.append("Built interactive AI applications.")

    if "fastapi" in matched_skills:
        strengths.append("Backend API development experience.")

    if "vector database" in matched_skills:
        strengths.append("Vector database knowledge.")

    if not strengths:
        strengths.append("Foundational technical skills identified.")

    # ==========================================
    # WEAKNESSES
    # ==========================================

    weaknesses = []

    if "docker" in missing_skills:
        weaknesses.append("Docker is commonly required for deployment.")

    if "gemini" in missing_skills:
        weaknesses.append("Gemini API experience is missing.")

    if not weaknesses:
        weaknesses.append("No major technical gaps detected.")

    # ==========================================
    # BUILD REPORT
    # ==========================================

    report = f"""
# 🎯 Job Match Analysis

### Target Role

**{target_role}**

---

## 📊 ATS Match Score

**{ats_score}/100**

### Hiring Recommendation

**{recommendation}**

---

## ✅ Matching Skills

"""

    if matched_skills:
        report += "\n".join(
            f"✓ {skill.title()}"
            for skill in matched_skills
        )
    else:
        report += "No matching skills detected."

    report += """

---

## ❌ Missing Skills

"""

    if missing_skills:
        report += "\n".join(
            f"✗ {skill.title()}"
            for skill in missing_skills
        )
    else:
        report += "No important skills missing."

    report += f"""

---

## 📈 Keyword Coverage

- JD Keywords: **{total}**
- Matched: **{matched}**
- Missing: **{len(missing_skills)}**

Coverage: **{ats_score}%**

---

## 💪 Strengths

"""

    report += "\n".join(
        f"• {point}"
        for point in strengths
    )

    report += """

---

## ⚠️ Improvement Areas

"""

    report += "\n".join(
        f"• {point}"
        for point in weaknesses
    )

    report += """

---

## 🚀 ATS Improvement Suggestions

"""

    if missing_skills:
        report += (
            "Build small projects demonstrating these skills before "
            "adding them to your resume.\n\n"
        )

    if "docker" in missing_skills:
        report += (
            "• Learn Docker by containerizing one of your FastAPI "
            "or Streamlit projects.\n"
        )

    if "gemini" in missing_skills:
        report += (
            "• Build a small Gemini-powered chatbot using the "
            "Google Gemini API.\n"
        )

    report += """

---

## 💼 Final Recommendation

"""

    if ats_score >= 90:
        report += (
            "Your resume is strongly aligned with this role. "
            "Focus on interview preparation."
        )

    elif ats_score >= 75:
        report += (
            "Your resume is a good match. "
            "Strengthen the remaining missing skills and "
            "highlight project achievements."
        )

    else:
        report += (
            "Improve your resume by addressing the missing "
            "skills and adding measurable project impact."
        )

    return {
        "job_match": report
    }