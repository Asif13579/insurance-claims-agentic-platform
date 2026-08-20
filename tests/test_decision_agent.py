import pytest

from app.agents.decision_agent import DecisionAgent


@pytest.mark.asyncio
async def test_decision_agent_returns_approved_response():

    agent = DecisionAgent()

    state = {
        "claim_id": "CLM-DEC-001",
        "customer_id": "CUS-001",
        "claim_decision": {
            "decision": "APPROVE",
            "reason": "Claim passed document and consistency validation.",
        },
    }

    result = await agent.process(state)

    assert result["final_response"]["status"] == "approved"
    assert result["final_response"]["message"] == (
        "Your claim has been approved."
    )


@pytest.mark.asyncio
async def test_decision_agent_returns_documents_required_response():

    agent = DecisionAgent()

    state = {
        "claim_id": "CLM-DEC-002",
        "customer_id": "CUS-002",
        "claim_decision": {
            "decision": "REQUEST_MORE_INFORMATION",
            "reason": "Required documents are missing.",
            "missing_documents": [
                "police_report",
            ],
        },
    }

    result = await agent.process(state)

    assert result["final_response"]["status"] == "documents_required"
    assert result["final_response"]["message"] == (
        "Additional documents are required."
    )
    assert result["final_response"]["missing_documents"] == [
        "police_report"
    ]


@pytest.mark.asyncio
async def test_decision_agent_returns_manual_review_response():

    agent = DecisionAgent()

    state = {
        "claim_id": "CLM-DEC-003",
        "customer_id": "CUS-003",
        "claim_decision": {
            "decision": "MANUAL_REVIEW",
            "reason": "Claim failed consistency validation.",
        },
    }

    result = await agent.process(state)

    assert result["final_response"]["status"] == "manual_review"
    assert result["final_response"]["message"] == (
        "Your claim requires manual review."
    )
    assert result["final_response"]["reason"] == (
        "Claim failed consistency validation."
    )


@pytest.mark.asyncio
async def test_decision_agent_handles_missing_decision():

    agent = DecisionAgent()

    state = {
        "claim_id": "CLM-DEC-004",
        "customer_id": "CUS-004",
        "customer_message": "I had a car accident.",
        "documents": [],
    }

    result = await agent.process(state)

    assert result["final_response"]["status"] == "error"
    assert result["final_response"]["message"] == (
        "Claim decision is unavailable."
    )


@pytest.mark.asyncio
async def test_decision_agent_preserves_state():

    agent = DecisionAgent()

    state = {
        "claim_id": "CLM-DEC-005",
        "customer_id": "CUS-005",
        "customer_message": "I had a car accident.",
        "documents": [],
        "customer_data": {
            "name": "Test Customer",
        },
        "claim_decision": {
            "decision": "APPROVE",
            "reason": "Claim passed validation.",
        },
    }

    result = await agent.process(state)

    assert result["claim_id"] == "CLM-DEC-005"
    assert result["customer_id"] == "CUS-005"
    assert result["customer_message"] == "I had a car accident."
    assert result["documents"] == []
    assert result["customer_data"]["name"] == "Test Customer"
    assert result["claim_decision"]["decision"] == "APPROVE"
    assert "final_response" in result
