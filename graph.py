from langgraph.graph import StateGraph, START, END

from state import AgentState

from agents.planner import planner_agent
from agents.resume_agent import resume_agent
from agents.skill_agent import skill_agent
from agents.interview_agent import interview_agent
from agents.job_match_agent import job_match_agent
from agents.final_agent import final_report_agent

from resume_rewrite_agent import resume_rewrite_agent


# =====================================================
# ROUTER
# =====================================================

def planner_router(state: AgentState):

    plan = state.get("plan", [])

    if "resume_agent" in plan:
        return "resume_agent"

    if "resume_rewrite_agent" in plan:
        return "resume_rewrite_agent"

    if "skill_agent" in plan:
        return "skill_agent"

    if "interview_agent" in plan:
        return "interview_agent"

    if "job_match_agent" in plan:
        return "job_match_agent"

    return "final_agent"


# =====================================================
# BUILD GRAPH
# =====================================================

def build_graph():

    workflow = StateGraph(AgentState)

    # Nodes
    workflow.add_node("planner", planner_agent)
    workflow.add_node("resume_agent", resume_agent)
    workflow.add_node(
        "resume_rewrite_agent",
        resume_rewrite_agent
    )
    workflow.add_node("skill_agent", skill_agent)
    workflow.add_node(
        "interview_agent",
        interview_agent
    )
    workflow.add_node(
        "job_match_agent",
        job_match_agent
    )
    workflow.add_node(
        "final_agent",
        final_report_agent
    )

    # Start
    workflow.add_edge(
        START,
        "planner"
    )

    # Planner decides first agent
    workflow.add_conditional_edges(
        "planner",
        planner_router,
        {
            "resume_agent": "resume_agent",
            "resume_rewrite_agent": "resume_rewrite_agent",
            "skill_agent": "skill_agent",
            "interview_agent": "interview_agent",
            "job_match_agent": "job_match_agent",
            "final_agent": "final_agent"
        }
    )

    # IMPORTANT:
    # For now, keep the existing complete pipeline
    # after the first selected agent.

    workflow.add_edge(
        "resume_agent",
        "resume_rewrite_agent"
    )

    workflow.add_edge(
        "resume_rewrite_agent",
        "skill_agent"
    )

    workflow.add_edge(
        "skill_agent",
        "interview_agent"
    )

    workflow.add_edge(
        "interview_agent",
        "job_match_agent"
    )

    workflow.add_edge(
        "job_match_agent",
        "final_agent"
    )

    workflow.add_edge(
        "final_agent",
        END
    )

    return workflow.compile()