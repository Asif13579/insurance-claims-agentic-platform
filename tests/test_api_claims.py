def test_create_approved_claim(client):
    payload = {
        "claim_id": "CLM-API-TEST-001",
        "customer_id": "CUS-API-TEST-001",
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

    assert data["claim_id"] == "CLM-API-TEST-001"
    assert data["customer_id"] == "CUS-API-TEST-001"
    assert data["status"] == "APPROVED"
    assert data["claim_complete"] is True
    assert data["claim_decision"]["decision"] == "APPROVE"
    assert data["final_response"]["status"] == "approved"


def test_create_claim_with_missing_documents(client):
    payload = {
        "claim_id": "CLM-API-TEST-002",
        "customer_id": "CUS-API-TEST-002",
        "customer_message": "I had a car accident.",
        "documents": [
            {
                "filename": "police_report.pdf",
                "document_type": "police_report",
            }
        ],
    }

    response = client.post("/claims", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["claim_id"] == "CLM-API-TEST-002"
    assert data["status"] == "NEEDS_DOCUMENTS"
    assert data["claim_complete"] is False
    assert data["claim_decision"]["decision"] == "REQUEST_MORE_INFORMATION"
    assert "repair_estimate" in data["claim_decision"]["missing_documents"]
    assert "photo" in data["claim_decision"]["missing_documents"]


def test_create_inconsistent_claim(client):
    payload = {
        "claim_id": "CLM-API-TEST-003",
        "customer_id": "CUS-API-TEST-003",
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

    assert data["claim_id"] == "CLM-API-TEST-003"
    assert data["claim_decision"]["decision"] == "MANUAL_REVIEW"
    assert data["claim_complete"] is False
    assert data["review"]["required"] is True
    assert data["review"]["recommended_action"] == "manual_review"
    assert data["final_response"]["status"] == "manual_review"


def test_get_existing_claim_after_creation(client):
    payload = {
        "claim_id": "CLM-API-TEST-004",
        "customer_id": "CUS-API-TEST-004",
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

    get_response = client.get("/claims/CLM-API-TEST-004")

    assert get_response.status_code == 200

    data = get_response.json()

    assert data == {
        "claim_id": "CLM-API-TEST-004",
        "customer_id": "CUS-API-TEST-004",
        "status": "APPROVED",
        "claim_complete": True,
        "final_decision": "APPROVE",
    }


def test_get_nonexistent_claim_returns_404(client):
    response = client.get("/claims/CLM-DOES-NOT-EXIST")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_duplicate_claim_id_returns_conflict(client):
    payload = {
        "claim_id": "CLM-DUPLICATE-001",
        "customer_id": "CUS-DUPLICATE-001",
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

    first_response = client.post("/claims", json=payload)

    assert first_response.status_code == 200

    second_response = client.post("/claims", json=payload)

    assert second_response.status_code == 409