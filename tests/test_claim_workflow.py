def test_inconsistent_claim_requires_review(client):

    payload = {
        "claim_id": "CLM-TEST-005",
        "customer_id": "CUS-005",
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

    response = client.post("/claims", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["claim_id"] == "CLM-TEST-005"
    assert data["status"] == "NEEDS_REVIEW"
    assert data["claim_complete"] is False


def test_complete_claim_returns_approve(client):

    payload = {
        "claim_id": "CLM-API-001",
        "customer_id": "CUS-API-001",
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

    response = client.post("/claims", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["claim_id"] == "CLM-API-001"
    assert data["claim_decision"]["decision"] == "APPROVE"


def test_missing_documents_requests_information(client):

    payload = {
        "claim_id": "CLM-API-002",
        "customer_id": "CUS-API-002",
        "customer_message": "I had a car accident.",
        "documents": [
            {
                "filename": "police_report.pdf",
                "document_type": "police_report"
            }
        ]
    }

    response = client.post("/claims", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert (
        data["claim_decision"]["decision"]
        == "REQUEST_MORE_INFORMATION"
    )


def test_wrong_document_returns_manual_review(client):

    payload = {
        "claim_id": "CLM-API-003",
        "customer_id": "CUS-API-003",
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

    response = client.post("/claims", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert (
        data["review"]["recommended_action"]
        == "manual_review"
    )


def test_complete_claim_runs_document_intelligence(client):

    payload = {
        "claim_id": "CLM-DOC-INT-001",
        "customer_id": "CUS-DOC-INT-001",
        "customer_message": "I had a car accident.",
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
    }

    response = client.post("/claims", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "document_results" in data
    assert len(data["document_results"]) == 3

    assert "extracted_data" in data
    assert "police_report" in data["extracted_data"]
    assert "repair_estimate" in data["extracted_data"]
    assert "photo" in data["extracted_data"]