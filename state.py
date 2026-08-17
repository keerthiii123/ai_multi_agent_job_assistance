from typing import TypedDict

class AgentState(TypedDict):

    user_query: str
    target_role: str
    resume_text: str
    job_description: str

    plan: list

    resume_analysis: str
    resume_rewrite: str
    skill_gap: str
    interview_questions: str
    job_match: str
    final_report: str