from state import AgentState


# =====================================================
# PLANNER AGENT
# =====================================================

def planner_agent(state: AgentState):

    user_query = state.get(
        "user_query",
        ""
    ).lower()

    job_description = state.get(
        "job_description",
        ""
    ).strip()

    plan = []


    # =====================================================
    # RESUME ANALYSIS
    # =====================================================

    resume_keywords = [
        "resume",
        "cv",
        "profile",
        "analyze my resume",
        "review my resume"
    ]

    if any(
        keyword in user_query
        for keyword in resume_keywords
    ):
        plan.append("resume_agent")


    # =====================================================
    # SKILL GAP ANALYSIS
    # =====================================================

    skill_keywords = [
        "skill gap",
        "skill gaps",
        "missing skills",
        "skills",
        "skill analysis"
    ]

    if any(
        keyword in user_query
        for keyword in skill_keywords
    ):

        if "skill_agent" not in plan:
            plan.append("skill_agent")


    # =====================================================
    # INTERVIEW PREPARATION
    # =====================================================

    interview_keywords = [
        "interview",
        "interview questions",
        "prepare interview",
        "prepare for interview"
    ]

    if any(
        keyword in user_query
        for keyword in interview_keywords
    ):

        if "interview_agent" not in plan:
            plan.append("interview_agent")


    # =====================================================
    # JOB MATCH ANALYSIS
    # =====================================================

    job_match_keywords = [
        "job match",
        "job matching",
        "match my resume",
        "compare my resume",
        "compare resume",
        "job description",
        "jd match",
        "match score"
    ]


    # =====================================================
    # IF JOB DESCRIPTION IS PROVIDED
    # AUTOMATICALLY RUN SKILL GAP + JOB MATCH
    # =====================================================

    if job_description:

        if "skill_agent" not in plan:
            plan.append("skill_agent")

        if "job_match_agent" not in plan:
            plan.append("job_match_agent")


    # =====================================================
    # IF USER SPECIFICALLY ASKS FOR JOB MATCH
    # =====================================================

    elif any(
        keyword in user_query
        for keyword in job_match_keywords
    ):

        if "job_match_agent" not in plan:
            plan.append("job_match_agent")


    # =====================================================
    # DEFAULT
    # =====================================================

    if not plan:
        plan.append("resume_agent")


    # =====================================================
    # SAVE PLAN
    # =====================================================

    return {
        "plan": plan
    }