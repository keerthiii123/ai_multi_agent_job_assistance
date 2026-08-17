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
        "review my resume",
        "resume analysis"
    ]

    resume_requested = any(
        keyword in user_query
        for keyword in resume_keywords
    )


    if resume_requested:

        plan.append("resume_agent")

        # Resume rewrite is useful when resume analysis is requested
        plan.append("resume_rewrite_agent")


    # =====================================================
    # SKILL GAP
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
    # INTERVIEW
    # =====================================================

    interview_keywords = [
        "interview",
        "interview questions",
        "prepare interview",
        "prepare for interview",
        "interview preparation"
    ]

    if any(
        keyword in user_query
        for keyword in interview_keywords
    ):

        if "interview_agent" not in plan:
            plan.append("interview_agent")


    # =====================================================
    # JOB MATCH
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


    if job_description:

        if "skill_agent" not in plan:
            plan.append("skill_agent")

        if "job_match_agent" not in plan:
            plan.append("job_match_agent")

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
    # FINAL REPORT
    # =====================================================

    # Final report is always useful after the selected analysis.
    plan.append("final_agent")


    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================

    unique_plan = []

    for agent in plan:

        if agent not in unique_plan:
            unique_plan.append(agent)


    # =====================================================
    # SAVE PLAN
    # =====================================================

    return {
        "plan": unique_plan
    }