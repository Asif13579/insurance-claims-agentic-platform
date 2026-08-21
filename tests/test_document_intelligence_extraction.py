import pytest

from app.agents.document_intelligence_agent import (
    DocumentIntelligenceAgent,
)


@pytest.mark.asyncio
async def test_extract_incident_date_and_vehicle():

    agent = DocumentIntelligenceAgent()

    state = {
        "valid_documents": [
            {
                "filename": "police_report.txt",
                "document_type": "police_report",
                "content": (
                    "Accident Date: 2026-08-10\n"
                    "Vehicle: Honda City\n"
                    "Location: Delhi"
                ),
            }
        ]
    }

    result = await agent.process(state)

    extraction = result["extracted_data"]["police_report"]

    assert extraction["incident_date"] == "2026-08-10"
    assert extraction["vehicle"] == "Honda City"
    assert extraction["incident_location"] == "Delhi"


@pytest.mark.asyncio
async def test_extract_repair_amount():

    agent = DocumentIntelligenceAgent()

    state = {
        "valid_documents": [
            {
                "filename": "repair_estimate.txt",
                "document_type": "repair_estimate",
                "content": (
                    "Estimated Repair Cost: ₹85,000"
                ),
            }
        ]
    }

    result = await agent.process(state)

    extraction = result["extracted_data"]["repair_estimate"]

    assert extraction["estimated_amount"] == 85000.0


@pytest.mark.asyncio
async def test_extract_multiple_fields():

    agent = DocumentIntelligenceAgent()

    state = {
        "valid_documents": [
            {
                "filename": "medical_report.txt",
                "document_type": "police_report",
                "content": (
                    "Accident Date: 2026-08-10\n"
                    "Location: Delhi\n"
                    "Vehicle: Maruti Swift\n"
                    "Incident Type: Collision"
                ),
            }
        ]
    }

    result = await agent.process(state)

    extraction = result["extracted_data"]["police_report"]

    assert extraction["incident_date"] == "2026-08-10"
    assert extraction["incident_location"] == "Delhi"
    assert extraction["vehicle"] == "Maruti Swift"
    assert extraction["incident_type"] == "Collision"


@pytest.mark.asyncio
async def test_empty_document_returns_null_fields():

    agent = DocumentIntelligenceAgent()

    state = {
        "valid_documents": [
            {
                "filename": "empty.txt",
                "document_type": "police_report",
                "content": "",
            }
        ]
    }

    result = await agent.process(state)

    extraction = result["extracted_data"]["police_report"]

    assert extraction["incident_date"] is None
    assert extraction["vehicle"] is None
    assert extraction["estimated_amount"] is None