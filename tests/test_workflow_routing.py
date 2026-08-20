from app.graph.workflow import route_after_consistency


def test_consistent_claim_routes_to_claim():

    state = {
        "consistency_check": {
            "consistent": True,
            "issues": []
        }
    }

    assert route_after_consistency(state) == "claim"


def test_inconsistent_claim_routes_to_review():

    state = {
        "consistency_check": {
            "consistent": False,
            "issues": [
                "Missing police report"
            ]
        }
    }

    assert route_after_consistency(state) == "review"


def test_missing_consistency_check_routes_to_review():

    state = {}

    assert route_after_consistency(state) == "review"

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_complete_claim_reaches_final_decision():

    payload = {
        "claim_id": "CLM-FULL-001",
        "customer_id": "CUS-FULL-001",
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

    assert data["claim_decision"]["decision"] == "APPROVE"
    assert "final_response" in data

def test_inconsistent_claim_reaches_review_and_final_decision():

    payload = {
        "claim_id": "CLM-FULL-002",
        "customer_id": "CUS-FULL-002",
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

    assert data["review"]["required"] is True
    assert data["claim_decision"]["decision"] == "MANUAL_REVIEW"
    assert "final_response" in data
