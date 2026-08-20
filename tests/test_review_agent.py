import pytest

from app.agents.review_agent import ReviewAgent


@pytest.mark.asyncio
async def test_review_agent_creates_manual_review():

    agent = ReviewAgent()

    state = {
        "claim_id": "CLM-REV-001",
        "customer_id": "CUS-001",
        "customer_message": "I had a car accident.",
        "documents": [],
        "consistency_check": {
            "consistent": False,
            "reason": "Required document is missing."
        }
    }

    result = await agent.process(state)

    assert result["review"]["required"] is True
    assert result["review"]["status"] == "pending"
    assert result["review"]["recommended_action"] == "manual_review"


@pytest.mark.asyncio
async def test_review_agent_records_consistency_reason():

    agent = ReviewAgent()

    state = {
        "claim_id": "CLM-REV-002",
        "consistency_check": {
            "consistent": False,
            "reason": "Passport document submitted instead of police report."
        }
    }

    result = await agent.process(state)

    assert result["review"]["reason"] == (
        "Passport document submitted instead of police report."
    )


@pytest.mark.asyncio
async def test_review_agent_handles_missing_consistency_check():

    agent = ReviewAgent()

    state = {
        "claim_id": "CLM-REV-003",
        "customer_id": "CUS-003",
        "documents": []
    }

    result = await agent.process(state)

    assert result["review"]["required"] is True
    assert result["review"]["status"] == "pending"


@pytest.mark.asyncio
async def test_review_agent_preserves_state():

    agent = ReviewAgent()

    state = {
        "claim_id": "CLM-REV-004",
        "customer_id": "CUS-004",
        "customer_message": "I had a car accident.",
        "documents": [],
        "consistency_check": {
            "consistent": False,
            "reason": "Missing documents."
        }
    }

    result = await agent.process(state)

    assert result["claim_id"] == "CLM-REV-004"
    assert result["customer_id"] == "CUS-004"
    assert result["customer_message"] == "I had a car accident."
