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


@pytest.mark.asyncio
async def test_consistency_agent_detects_conflicting_document_data():

    agent = ConsistencyAgent()

    state = {
        "claim_id": "CLM-CON-005",

        "customer_data": {
            "incident_type": "vehicle_accident",
            "incident_date": "2026-08-15",
            "incident_location": "Bangalore",
        },

        "documents": [
            {
                "filename": "police_report.pdf",
                "document_type": "police_report",
            },
            {
                "filename": "repair_estimate.pdf",
                "document_type": "repair_estimate",
            },
            {
                "filename": "car_photo.jpg",
                "document_type": "photo",
            },
        ],

        "extracted_data": {
            "police_report": {
                "incident_type": "vehicle_accident",
                "incident_date": "2026-08-20",
                "incident_location": "Bangalore",
            }
        },
    }

    result = await agent.process(state)

    consistency = result["consistency_check"]

    assert consistency["consistent"] is False

    assert any(
        "incident_date" in issue
        for issue in consistency["issues"]
    )


@pytest.mark.asyncio
async def test_consistency_agent_accepts_matching_extracted_data():

    agent = ConsistencyAgent()

    state = {
        "claim_id": "CLM-CON-006",

        "customer_data": {
            "incident_type": "vehicle_accident",
            "incident_date": "2026-08-15",
            "incident_location": "Bangalore",
        },

        "documents": [
            {
                "filename": "police_report.pdf",
                "document_type": "police_report",
            },
            {
                "filename": "repair_estimate.pdf",
                "document_type": "repair_estimate",
            },
            {
                "filename": "car_photo.jpg",
                "document_type": "photo",
            },
        ],

        "extracted_data": {
            "police_report": {
                "incident_type": "vehicle_accident",
                "incident_date": "2026-08-15",
                "incident_location": "Bangalore",
            }
        },
    }

    result = await agent.process(state)

    assert result["consistency_check"]["consistent"] is True
    assert result["consistency_check"]["issues"] == []


@pytest.mark.asyncio
async def test_consistency_agent_detects_conflicting_document_data():

    agent = ConsistencyAgent()

    state = {
        "claim_id": "CLM-CON-005",
        "documents": [
            {
                "filename": "police_report.pdf",
                "document_type": "police_report",
            },
            {
                "filename": "repair_estimate.pdf",
                "document_type": "repair_estimate",
            },
            {
                "filename": "car_photo.jpg",
                "document_type": "photo",
            },
        ],
        "extracted_data": {
            "police_report": {
                "incident_date": "2026-08-10",
                "vehicle": "Honda City",
            },
            "repair_estimate": {
                "incident_date": "2026-08-12",
                "vehicle": "Honda City",
            },
            "photo": {},
        },
    }

    result = await agent.process(state)

    assert result["consistency_check"]["consistent"] is False

    assert any(
        "Conflicting incident dates" in issue
        for issue in result["consistency_check"]["issues"]
    )


@pytest.mark.asyncio
async def test_consistency_agent_accepts_matching_extracted_data():

    agent = ConsistencyAgent()

    state = {
        "claim_id": "CLM-CON-006",
        "documents": [
            {
                "filename": "police_report.pdf",
                "document_type": "police_report",
            },
            {
                "filename": "repair_estimate.pdf",
                "document_type": "repair_estimate",
            },
            {
                "filename": "car_photo.jpg",
                "document_type": "photo",
            },
        ],
        "extracted_data": {
            "police_report": {
                "incident_date": "2026-08-10",
                "vehicle": "Honda City",
            },
            "repair_estimate": {
                "incident_date": "2026-08-10",
                "vehicle": "Honda City",
            },
            "photo": {},
        },
    }

    result = await agent.process(state)

    assert result["consistency_check"]["consistent"] is True
    assert result["consistency_check"]["issues"] == []


@pytest.mark.asyncio
async def test_consistency_agent_detects_customer_document_mismatch():

    agent = ConsistencyAgent()

    state = {
        "claim_id": "CLM-CON-007",
        "documents": [
            {
                "filename": "police_report.pdf",
                "document_type": "police_report",
            },
            {
                "filename": "repair_estimate.pdf",
                "document_type": "repair_estimate",
            },
            {
                "filename": "car_photo.jpg",
                "document_type": "photo",
            },
        ],
        "customer_data": {
            "accident_date": "2026-08-10",
        },
        "extracted_data": {
            "police_report": {
                "incident_date": "2026-08-12",
            },
            "repair_estimate": {
                "incident_date": "2026-08-12",
            },
            "photo": {},
        },
    }

    result = await agent.process(state)

    assert result["consistency_check"]["consistent"] is False

    assert any(
        "Customer data conflicts" in issue
        for issue in result["consistency_check"]["issues"]
    )