from state import AgentState
from llm import invoke_llm

# =====================================================
# RESUME REWRITE AGENT
# =====================================================

def resume_rewrite_agent(state: AgentState):

    resume = state.get("resume_text", "")
    role = state.get("target_role", "")

    if not resume.strip():
        return {
            "resume_rewrite": "Resume not available."
        }

    prompt = f"""
You are an ATS Resume Expert.

Target Role:
{role}

Rewrite the resume professionally.

Instructions:
- Keep all information truthful.
- Do not invent experience.
- Improve ATS keywords.
- Improve formatting.
- Strengthen project descriptions.
- Add action verbs.
- Keep it suitable for a one-page resume.
- Return only the rewritten resume in Markdown.

Resume:
{resume}
"""

    try:
        rewritten = invoke_llm(prompt)
    except Exception as e:
        rewritten = f"Resume rewrite failed: {e}"

    return {
        "resume_rewrite": rewritten
    }