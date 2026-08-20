import pytest

from app.agents.claim_agent import ClaimAgent


@pytest.mark.asyncio
async def test_claim_agent_approves_complete_claim():

    agent = ClaimAgent()

    state = {
        "claim_id": "CLM-CLAIM-001",
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
        ],
        "consistency_check": {
            "consistent": True
        }
    }

    result = await agent.process(state)

    assert result["claim_decision"]["decision"] == "APPROVE"


@pytest.mark.asyncio
async def test_claim_agent_requests_missing_documents():

    agent = ClaimAgent()

    state = {
        "claim_id": "CLM-CLAIM-002",
        "documents": [
            {
                "filename": "police_report.pdf",
                "document_type": "police_report"
            }
        ],
        "consistency_check": {
            "consistent": True
        }
    }

    result = await agent.process(state)

    assert result["claim_decision"]["decision"] == "REQUEST_MORE_INFORMATION"
    assert "photo" in result["claim_decision"]["missing_documents"]
    assert "repair_estimate" in result["claim_decision"]["missing_documents"]


@pytest.mark.asyncio
async def test_claim_agent_sends_inconsistent_claim_to_review():

    agent = ClaimAgent()

    state = {
        "claim_id": "CLM-CLAIM-003",
        "documents": [],
        "consistency_check": {
            "consistent": False,
            "reason": "Invalid document."
        }
    }

    result = await agent.process(state)

    assert result["claim_decision"]["decision"] == "MANUAL_REVIEW"


@pytest.mark.asyncio
async def test_claim_agent_preserves_state():

    agent = ClaimAgent()

    state = {
        "claim_id": "CLM-CLAIM-004",
        "customer_id": "CUS-004",
        "customer_message": "I had a car accident.",
        "documents": [],
        "consistency_check": {
            "consistent": False
        }
    }

    result = await agent.process(state)

    assert result["claim_id"] == "CLM-CLAIM-004"
    assert result["customer_id"] == "CUS-004"
    assert result["customer_message"] == "I had a car accident."
    assert "claim_decision" in result


@pytest.mark.asyncio
async def test_claim_agent_approves_matching_extracted_data():

    agent = ClaimAgent()

    state = {
        "valid_documents": [
            {"filename": "police.pdf", "document_type": "police_report"},
            {"filename": "estimate.pdf", "document_type": "repair_estimate"},
            {"filename": "photo.jpg", "document_type": "photo"},
        ],
        "invalid_documents": [],
        "missing_documents": [],
        "consistency_check": {
            "consistent": True,
            "issues": [],
            "reason": "Claim documents are consistent.",
        },
        "extracted_data": {
            "repair_estimate": {
                "estimated_amount": 45000.0,
                "incident_date": "2026-08-10",
            },
            "police_report": {
                "incident_date": "2026-08-10",
            },
        },
    }

    result = await agent.process(state)

    assert result["claim_decision"]["decision"] == "APPROVE"


@pytest.mark.asyncio
async def test_claim_agent_rejects_conflicting_extracted_data():

    agent = ClaimAgent()

    state = {
        "valid_documents": [
            {"filename": "police.pdf", "document_type": "police_report"},
            {"filename": "estimate.pdf", "document_type": "repair_estimate"},
            {"filename": "photo.jpg", "document_type": "photo"},
        ],
        "invalid_documents": [],
        "missing_documents": [],
        "consistency_check": {
            "consistent": False,
            "issues": [
                "Incident dates conflict between documents."
            ],
            "reason": "Incident dates conflict between documents.",
        },
        "extracted_data": {
            "repair_estimate": {
                "incident_date": "2026-08-10",
            },
            "police_report": {
                "incident_date": "2026-08-15",
            },
        },
    }

    result = await agent.process(state)

    assert result["claim_decision"]["decision"] == "MANUAL_REVIEW"