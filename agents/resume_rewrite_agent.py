from state import AgentState
from llm import invoke_llm


# =====================================================
# RESUME REWRITE AGENT
# =====================================================

def resume_rewrite_agent(state: AgentState):

    resume = state.get("resume_text", "").strip()
    role = state.get("target_role", "AI Engineer")

    # -------------------------------------------------
    # Resume validation
    # -------------------------------------------------

    if not resume:

        return {
            "resume_rewrite": (
                "## Resume Rewrite\n\n"
                "Resume not available."
            )
        }

    # -------------------------------------------------
    # LLM Prompt
    # -------------------------------------------------

    prompt = f"""
You are an expert ATS Resume Writer and AI Engineering
Recruiter.

Target Role:
{role}

Original Resume:
{resume}

Your task is to rewrite the resume professionally for
the target role.

IMPORTANT RULES:

1. Do NOT invent any information.
2. Do NOT create fake companies, projects, skills,
   certifications, experience, or achievements.
3. Keep the candidate's actual education and experience.
4. Improve ATS keyword alignment.
5. Use strong professional action verbs.
6. Improve project descriptions.
7. Make technical skills easy for ATS systems to detect.
8. Keep the resume concise and professional.
9. Prefer a one-page resume format.
10. Do not add unnecessary explanations.
11. Do not mention that you are an AI.
12. Return ONLY the rewritten resume in Markdown.

Recommended structure:

# Candidate Name

## Professional Summary

## Technical Skills

## Projects

## Experience

## Education

## Certifications

Only include sections when the information exists
in the original resume.

For projects:
- Explain what was built.
- Mention technologies actually used.
- Mention the candidate's actual contribution.
- Use measurable results only when they exist
  in the original resume.

For experience:
- Use strong action verbs.
- Keep responsibilities truthful.
- Do not exaggerate.

Target the resume toward:
{role}
"""

    # -------------------------------------------------
    # Call LLM
    # -------------------------------------------------

    try:

        rewritten = invoke_llm(prompt)

    except Exception as e:

        return {
            "resume_rewrite": (
                "## Resume Rewrite\n\n"
                f"Resume rewrite failed: {str(e)}"
            )
        }

    # -------------------------------------------------
    # Handle LLM errors
    # -------------------------------------------------

    if not rewritten:

        rewritten = (
            "## Resume Rewrite\n\n"
            "Unable to generate the rewritten resume."
        )

    # -------------------------------------------------
    # Return State Update
    # -------------------------------------------------

    return {
        "resume_rewrite": rewritten.strip()
    }