from langgraph.graph import StateGraph, START, END

from state import AgentState

from agents.planner import planner_agent
from agents.resume_agent import resume_agent
from agents.resume_rewrite_agent import resume_rewrite_agent
from agents.skill_agent import skill_agent
from agents.interview_agent import interview_agent
from agents.job_match_agent import job_match_agent
from agents.final_agent import final_report_agent


# =====================================================
# AGENT ORDER
# =====================================================

AGENT_ORDER = [
    "resume_agent",
    "resume_rewrite_agent",
    "skill_agent",
    "interview_agent",
    "job_match_agent"
]


# =====================================================
# PLANNER ROUTER
# =====================================================

def planner_router(state: AgentState):

    plan = state.get("plan", [])

    if not plan:
        return "final_agent"

    # First selected agent
    for agent in AGENT_ORDER:

        if agent in plan:
            return agent

    return "final_agent"


# =====================================================
# NEXT AGENT ROUTER
# =====================================================

def next_agent_router(state: AgentState):

    plan = state.get("plan", [])

    completed = state.get(
        "completed_agents",
        []
    )

    # Find next agent from planner's plan
    for agent in AGENT_ORDER:

        if agent in plan and agent not in completed:
            return agent

    # Nothing left
    return "final_agent"


# =====================================================
# MARK AGENT AS COMPLETED
# =====================================================

def mark_completed(agent_name):

    def wrapper(state: AgentState):

        completed = list(
            state.get(
                "completed_agents",
                []
            )
        )

        if agent_name not in completed:
            completed.append(agent_name)

        return {
            "completed_agents": completed
        }

    return wrapper


# =====================================================
# BUILD GRAPH
# =====================================================

def build_graph():

    workflow = StateGraph(AgentState)


    # =================================================
    # NODES
    # =================================================

    workflow.add_node(
        "planner",
        planner_agent
    )

    workflow.add_node(
        "resume_agent",
        resume_agent
    )

    workflow.add_node(
        "resume_rewrite_agent",
        resume_rewrite_agent
    )

    workflow.add_node(
        "skill_agent",
        skill_agent
    )

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


    # =================================================
    # START → PLANNER
    # =================================================

    workflow.add_edge(
        START,
        "planner"
    )


    # =================================================
    # PLANNER → FIRST SELECTED AGENT
    # =================================================

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


    # =================================================
    # AGENT → NEXT AGENT
    # =================================================

    for agent_name in AGENT_ORDER:

        workflow.add_conditional_edges(
            agent_name,
            lambda state, name=agent_name:
                next_agent_router(
                    {
                        **state,
                        "completed_agents": list(
                            state.get(
                                "completed_agents",
                                []
                            )
                        ) + [name]
                    }
                ),
            {
                "resume_agent": "resume_agent",
                "resume_rewrite_agent": "resume_rewrite_agent",
                "skill_agent": "skill_agent",
                "interview_agent": "interview_agent",
                "job_match_agent": "job_match_agent",
                "final_agent": "final_agent"
            }
        )


    # =================================================
    # FINAL → END
    # =================================================

    workflow.add_edge(
        "final_agent",
        END
    )


    # =================================================
    # COMPILE
    # =================================================

    return workflow.compile()