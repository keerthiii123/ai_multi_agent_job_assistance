from state import AgentState


# =====================================================
# FINAL JOB READINESS REPORT
# =====================================================

def final_report_agent(state: AgentState):

    target_role = state.get(
        "target_role",
        "Not specified"
    )

    resume_analysis = state.get(
        "resume_analysis",
        ""
    )

    skill_gap = state.get(
        "skill_gap",
        ""
    )

    interview_questions = state.get(
        "interview_questions",
        ""
    )

    job_match = state.get(
        "job_match",
        ""
    )

    # =================================================
    # BUILD FINAL REPORT
    # =================================================

    report = f"""
# 🎯 FINAL JOB READINESS REPORT

## Target Role

**{target_role}**

==================================================
RESUME ANALYSIS
==================================================

{resume_analysis if resume_analysis else "Not requested."}


==================================================
SKILL GAP ANALYSIS
==================================================

{skill_gap if skill_gap else "Not requested."}


==================================================
JOB MATCH ANALYSIS
==================================================

{job_match if job_match else "Not requested."}


==================================================
INTERVIEW PREPARATION
==================================================

{interview_questions if interview_questions else "Not requested."}


==================================================
FINAL RECOMMENDATION
==================================================

### 1. Resume

Improve the resume by adding:

- Relevant technical skills
- Detailed project descriptions
- Measurable achievements
- Role-specific keywords
- Technologies used in real projects


### 2. Skills

Prioritize the missing skills identified
for the target role.

Focus on practical hands-on projects rather
than only theoretical learning.


### 3. Interview

Prepare answers for:

- HR questions
- Technical questions
- Resume-based questions
- Project questions
- Scenario-based questions
- Job-description-based questions


### 4. Job Application

Before applying, compare your resume with
the job description and add relevant keywords
that accurately represent your actual skills.


### 5. Final Advice

Build 1-2 strong AI Engineer projects that
demonstrate practical experience with:

- Python
- LangChain
- LangGraph
- RAG
- Vector Database
- FastAPI
- Docker
- Generative AI

Do not add technologies to your resume unless
you have genuinely learned or used them.
"""

    return {
        "final_report": report
    }