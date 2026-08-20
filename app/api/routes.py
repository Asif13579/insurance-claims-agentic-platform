from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.claim_schema import ClaimProcessRequest
from app.services.claim_service import ClaimService


router = APIRouter(
    prefix="/claims",
    tags=["Claims"],
)


@router.post("")
async def process_claim(
    request: ClaimProcessRequest,
    db: Session = Depends(get_db),
):
    service = ClaimService(db)

    state = {
        "claim_id": request.claim_id,
        "customer_id": request.customer_id,
        "customer_message": request.customer_message,
        "documents": [
            document.model_dump()
            for document in request.documents
        ],
        "status": "RECEIVED",
        "valid_documents": [],
        "invalid_documents": [],
        "missing_documents": [],
        "inconsistencies": [],
        "claim_complete": False,
        "final_claim": None,
    }

    result = await service.process_claim(state)

    return result


@router.get("/{claim_id}")
def get_claim(
    claim_id: str,
    db: Session = Depends(get_db),
):
    service = ClaimService(db)

    claim = service.get_claim(claim_id)

    if not claim:
        raise HTTPException(
            status_code=404,
            detail=f"Claim {claim_id} not found",
        )

    return {
        "claim_id": claim.claim_id,
        "customer_id": claim.customer_id,
        "status": claim.status,
        "claim_complete": claim.claim_complete == "true",
        "final_decision": claim.final_decision,
    }
