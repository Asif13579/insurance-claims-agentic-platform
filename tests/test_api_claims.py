from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_post_claim_with_complete_documents():
    payload = {
        "claim_id": "CLM-API-001",
        "customer_id": "CUS-API-001",
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

    assert data["claim_id"] == "CLM-API-001"
    assert data["customer_id"] == "CUS-API-001"

    assert data["claim_decision"]["decision"] == "APPROVE"

    assert data["final_response"]["status"] == "approved"

    assert data["status"] == "APPROVED"
    assert data["claim_complete"] is True


def test_post_claim_with_missing_documents():
    payload = {
        "claim_id": "CLM-API-002",
        "customer_id": "CUS-API-002",
        "customer_message": "I had a car accident.",
        "documents": [
            {
                "filename": "police_report.pdf",
                "document_type": "police_report",
            },
        ],
    }

    response = client.post("/claims", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["claim_id"] == "CLM-API-002"

    assert (
        data["claim_decision"]["decision"]
        == "REQUEST_MORE_INFORMATION"
    )

    assert data["final_response"]["status"] == "documents_required"

    assert data["claim_complete"] is False

    assert "repair_estimate" in data["claim_decision"]["missing_documents"]
    assert "photo" in data["claim_decision"]["missing_documents"]


def test_post_claim_with_wrong_document():
    payload = {
        "claim_id": "CLM-API-003",
        "customer_id": "CUS-API-003",
        "customer_message": "I had a car accident.",
        "documents": [
            {
                "filename": "passport.pdf",
                "document_type": "passport",
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

    assert data["claim_id"] == "CLM-API-003"

    assert data["claim_decision"]["decision"] == "MANUAL_REVIEW"

    assert data["final_response"]["status"] == "manual_review"

    assert data["review"]["required"] is True

    assert data["review"]["recommended_action"] == "manual_review"

    assert data["claim_complete"] is False


def test_get_claim():
    # Create the claim first.
    payload = {
        "claim_id": "CLM-API-GET-001",
        "customer_id": "CUS-API-GET-001",
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

    post_response = client.post("/claims", json=payload)

    assert post_response.status_code == 200

    # Retrieve the claim.
    response = client.get("/claims/CLM-API-GET-001")

    assert response.status_code == 200

    data = response.json()

    assert data["claim_id"] == "CLM-API-GET-001"
    assert data["customer_id"] == "CUS-API-GET-001"

    assert data["status"] == "APPROVED"
    assert data["claim_complete"] is True
    assert data["final_decision"] == "APPROVE"


def test_get_claim_not_found():
    response = client.get("/claims/CLM-DOES-NOT-EXIST")

    assert response.status_code == 404

    data = response.json()

    assert "detail" in data
    assert "CLM-DOES-NOT-EXIST" in data["detail"]