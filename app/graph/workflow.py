from langgraph.graph import StateGraph, END

from app.models.claim_state import ClaimState
from app.a2a.server import create_a2a_client


a2a = create_a2a_client()


async def intake_node(state: ClaimState) -> ClaimState:
    return await a2a.send("intake_agent", state)


async def document_node(state: ClaimState) -> ClaimState:
    return await a2a.send("document_agent", state)


async def document_intelligence_node(
    state: ClaimState,
) -> ClaimState:
    return await a2a.send(
        "document_intelligence_agent",
        state,
    )


async def consistency_node(state: ClaimState) -> ClaimState:
    return await a2a.send("consistency_agent", state)


async def claim_node(state: ClaimState) -> ClaimState:
    return await a2a.send("claim_agent", state)


async def review_node(state: ClaimState) -> ClaimState:
    return await a2a.send("review_agent", state)


async def decision_node(state: ClaimState) -> ClaimState:
    return await a2a.send("decision_agent", state)


def route_after_documents(state: ClaimState) -> str:
    """
    Missing required documents should skip consistency/review
    and go directly to the final decision.
    """

    if state.get("missing_documents"):
        return "decision"

    return "consistency"


def route_after_consistency(state: ClaimState) -> str:
    consistency_check = state.get("consistency_check") or {}

    if consistency_check.get("consistent") is True:
        return "claim"

    return "review"


def build_claim_graph():

    graph = StateGraph(ClaimState)

    # Nodes
    graph.add_node("intake", intake_node)
    graph.add_node("documents", document_node)
    graph.add_node(
        "document_intelligence",
        document_intelligence_node,
    )
    graph.add_node("consistency", consistency_node)
    graph.add_node("claim", claim_node)
    graph.add_node("review", review_node)
    graph.add_node("decision", decision_node)

    # Entry
    graph.set_entry_point("intake")

    # Intake → document validation
    graph.add_edge("intake", "documents")

    # Document validation → intelligence
    graph.add_edge(
        "documents",
        "document_intelligence",
    )

    # Missing documents bypass consistency/review
    graph.add_conditional_edges(
        "document_intelligence",
        route_after_documents,
        {
            "decision": "decision",
            "consistency": "consistency",
        },
    )

    # Consistency → claim/review
    graph.add_conditional_edges(
        "consistency",
        route_after_consistency,
        {
            "claim": "claim",
            "review": "review",
        },
    )

    # Final decision
    graph.add_edge("claim", "decision")
    graph.add_edge("review", "decision")

    graph.add_edge("decision", END)

    return graph.compile()
