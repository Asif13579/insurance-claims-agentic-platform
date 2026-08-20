import pytest

from app.agents.consistency_agent import ConsistencyAgent


@pytest.mark.asyncio
async def test_consistency_agent_accepts_consistent_claim():

    agent = ConsistencyAgent()

    state = {
        "claim_id": "CLM-CON-001",
        "customer_message": "I had a car accident.",
        "documents": [
            {
                "filename": "police_report.pdf",
                "document_type": "police_report"
            },
            {
                "filename": "repair_estimate.pdf",
                "document_type": "repair_estimate"
            },
            {
                "filename": "car_photo.jpg",
                "document_type": "photo"
            }
        ]
    }

    result = await agent.process(state)

    assert result["consistency_check"]["consistent"] is True
    assert result["consistency_check"]["issues"] == []


@pytest.mark.asyncio
async def test_consistency_agent_detects_missing_documents():

    agent = ConsistencyAgent()

    state = {
        "claim_id": "CLM-CON-002",
        "customer_message": "I had a car accident.",
        "documents": [
            {
                "filename": "police_report.pdf",
                "document_type": "police_report"
            }
        ]
    }

    result = await agent.process(state)

    assert result["consistency_check"]["consistent"] is False
    assert len(result["consistency_check"]["issues"]) > 0


@pytest.mark.asyncio
async def test_consistency_agent_detects_wrong_document():

    agent = ConsistencyAgent()

    state = {
        "claim_id": "CLM-CON-003",
        "customer_message": "I had a car accident.",
        "documents": [
            {
                "filename": "passport.pdf",
                "document_type": "passport"
            },
            {
                "filename": "repair_estimate.pdf",
                "document_type": "repair_estimate"
            },
            {
                "filename": "car_photo.jpg",
                "document_type": "photo"
            }
        ]
    }

    result = await agent.process(state)

    assert result["consistency_check"]["consistent"] is False


@pytest.mark.asyncio
async def test_consistency_agent_preserves_state():

    agent = ConsistencyAgent()

    state = {
        "claim_id": "CLM-CON-004",
        "customer_id": "CUS-004",
        "customer_message": "I had a car accident.",
        "documents": []
    }

    result = await agent.process(state)

    assert result["claim_id"] == "CLM-CON-004"
    assert result["customer_id"] == "CUS-004"
    assert "consistency_check" in result
