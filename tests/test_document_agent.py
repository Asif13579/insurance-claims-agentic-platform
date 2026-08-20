import pytest

from app.agents.document_agent import DocumentAgent


@pytest.mark.asyncio
async def test_document_agent_accepts_complete_documents():

    agent = DocumentAgent()

    state = {
        "claim_id": "CLM-DOC-001",
        "customer_id": "CUS-001",
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

    assert len(result["valid_documents"]) == 3
    assert result["invalid_documents"] == []
    assert result["missing_documents"] == []
    assert result["status"] == "DOCUMENTS_REVIEWED"


@pytest.mark.asyncio
async def test_document_agent_detects_missing_documents():

    agent = DocumentAgent()

    state = {
        "claim_id": "CLM-DOC-002",
        "customer_id": "CUS-002",
        "documents": [
            {
                "filename": "police_report.pdf",
                "document_type": "police_report"
            }
        ]
    }

    result = await agent.process(state)

    assert len(result["valid_documents"]) == 1
    assert result["invalid_documents"] == []

    assert "repair_estimate" in result["missing_documents"]
    assert "photo" in result["missing_documents"]

    assert result["status"] == "NEEDS_DOCUMENTS"


@pytest.mark.asyncio
async def test_document_agent_rejects_wrong_document():

    agent = DocumentAgent()

    state = {
        "claim_id": "CLM-DOC-003",
        "customer_id": "CUS-003",
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

    assert len(result["valid_documents"]) == 2
    assert len(result["invalid_documents"]) == 1

    assert result["invalid_documents"][0]["filename"] == "passport.pdf"
    assert result["invalid_documents"][0]["document_type"] == "passport"
    assert result["invalid_documents"][0]["reason"] == "Unsupported document type"

    assert "police_report" in result["missing_documents"]
    assert result["status"] == "NEEDS_DOCUMENTS"


@pytest.mark.asyncio
async def test_document_agent_handles_no_documents():

    agent = DocumentAgent()

    state = {
        "claim_id": "CLM-DOC-004",
        "customer_id": "CUS-004",
        "documents": []
    }

    result = await agent.process(state)

    assert result["valid_documents"] == []
    assert result["invalid_documents"] == []

    assert set(result["missing_documents"]) == {
        "police_report",
        "repair_estimate",
        "photo"
    }

    assert result["status"] == "NEEDS_DOCUMENTS"


@pytest.mark.asyncio
async def test_document_agent_rejects_missing_filename():

    agent = DocumentAgent()

    state = {
        "claim_id": "CLM-DOC-005",
        "customer_id": "CUS-005",
        "documents": [
            {
                "filename": "",
                "document_type": "police_report"
            }
        ]
    }

    result = await agent.process(state)

    assert len(result["invalid_documents"]) == 1

    assert result["invalid_documents"][0]["reason"] == (
        "Missing filename or document type"
    )

    assert "police_report" in result["missing_documents"]
    assert result["status"] == "NEEDS_DOCUMENTS"
