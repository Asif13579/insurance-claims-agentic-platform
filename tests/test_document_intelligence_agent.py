import pytest

from app.agents.document_intelligence_agent import (
    DocumentIntelligenceAgent,
)


@pytest.mark.asyncio
async def test_document_intelligence_processes_police_report():

    agent = DocumentIntelligenceAgent()

    state = {
        "claim_id": "CLM-DI-001",
        "customer_id": "CUS-DI-001",
        "valid_documents": [
            {
                "filename": "police_report.pdf",
                "document_type": "police_report",
            }
        ],
    }

    result = await agent.process(state)

    assert len(result["document_results"]) == 1

    document_result = result["document_results"][0]

    assert document_result["filename"] == "police_report.pdf"
    assert document_result["document_type"] == "police_report"
    assert document_result["valid"] is True
    assert document_result["errors"] == []
    assert document_result["extraction"] is not None


@pytest.mark.asyncio
async def test_document_intelligence_processes_repair_estimate():

    agent = DocumentIntelligenceAgent()

    state = {
        "claim_id": "CLM-DI-002",
        "valid_documents": [
            {
                "filename": "repair_estimate.pdf",
                "document_type": "repair_estimate",
            }
        ],
    }

    result = await agent.process(state)

    document_result = result["document_results"][0]

    assert document_result["filename"] == "repair_estimate.pdf"
    assert document_result["document_type"] == "repair_estimate"
    assert document_result["valid"] is True


@pytest.mark.asyncio
async def test_document_intelligence_processes_photo():

    agent = DocumentIntelligenceAgent()

    state = {
        "claim_id": "CLM-DI-003",
        "valid_documents": [
            {
                "filename": "car_photo.jpg",
                "document_type": "photo",
            }
        ],
    }

    result = await agent.process(state)

    document_result = result["document_results"][0]

    assert document_result["filename"] == "car_photo.jpg"
    assert document_result["document_type"] == "photo"
    assert document_result["valid"] is True


@pytest.mark.asyncio
async def test_document_intelligence_rejects_unsupported_document():

    agent = DocumentIntelligenceAgent()

    state = {
        "claim_id": "CLM-DI-004",
        "valid_documents": [
            {
                "filename": "passport.pdf",
                "document_type": "passport",
            }
        ],
    }

    result = await agent.process(state)

    document_result = result["document_results"][0]

    assert document_result["filename"] == "passport.pdf"
    assert document_result["document_type"] == "passport"
    assert document_result["valid"] is False

    assert document_result["errors"] == [
        "Unsupported document type"
    ]


@pytest.mark.asyncio
async def test_document_intelligence_handles_missing_metadata():

    agent = DocumentIntelligenceAgent()

    state = {
        "claim_id": "CLM-DI-005",
        "valid_documents": [
            {
                "filename": "",
                "document_type": "police_report",
            }
        ],
    }

    result = await agent.process(state)

    document_result = result["document_results"][0]

    assert document_result["valid"] is False

    assert document_result["errors"] == [
        "Missing filename or document type"
    ]


@pytest.mark.asyncio
async def test_document_intelligence_processes_multiple_documents():

    agent = DocumentIntelligenceAgent()

    state = {
        "claim_id": "CLM-DI-006",
        "valid_documents": [
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
    }

    result = await agent.process(state)

    assert len(result["document_results"]) == 3

    assert set(result["extracted_data"].keys()) == {
        "police_report",
        "repair_estimate",
        "photo",
    }


@pytest.mark.asyncio
async def test_document_intelligence_preserves_existing_state():

    agent = DocumentIntelligenceAgent()

    state = {
        "claim_id": "CLM-DI-007",
        "customer_id": "CUS-DI-007",
        "customer_message": "I had a car accident.",
        "status": "DOCUMENTS_REVIEWED",
        "customer_data": {
            "incident_type": "vehicle_accident"
        },
        "valid_documents": [
            {
                "filename": "police_report.pdf",
                "document_type": "police_report",
            }
        ],
    }

    result = await agent.process(state)

    assert result["claim_id"] == "CLM-DI-007"
    assert result["customer_id"] == "CUS-DI-007"
    assert result["customer_message"] == "I had a car accident."
    assert result["status"] == "DOCUMENTS_REVIEWED"

    assert result["customer_data"] == {
        "incident_type": "vehicle_accident"
    }

    assert "document_results" in result
    assert "extracted_data" in result
