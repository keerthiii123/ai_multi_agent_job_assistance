from state import AgentState
from llm import invoke_llm

# ==========================================
# INTERVIEW AGENT
# ==========================================

def interview_agent(state: AgentState):

    resume = state.get("resume_text", "")
    role = state.get("target_role", "AI Engineer")
    jd = state.get("job_description", "")
    difficulty = state.get("difficulty", "Medium")

    prompt = f"""
You are an expert AI Technical Interviewer.

Generate interview questions based on:

Target Role: {role}
Difficulty: {difficulty}

Resume:
{resume}

Job Description:
{jd}

Requirements:

1. Organize the interview into sections:
- HR
- Python
- Generative AI
- LangChain
- LangGraph
- RAG
- Project-Based
- Job Description-Based
- Scenario-Based

2. Generate questions according to difficulty.

Easy:
- Basic concepts

Medium:
- Practical implementation

Hard:
- Real-world debugging and system design

3. For every question include:
- Question
- What interviewer expects
- Short sample answer

4. Base questions on the resume whenever possible.

5. Use Markdown formatting.
"""

    response = invoke_llm(prompt)

    if not response:
        response = """
## Interview Questions

Unable to generate interview questions.
Please try again.
"""

    return {
        "interview_questions": response
    }