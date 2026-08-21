from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.config.database import get_db
from app.schemas.claim_schema import ClaimProcessRequest
from app.services.claim_service import ClaimService
from app.schemas.claim_response_schema import (
    ClaimResponse,
    ClaimSummaryResponse,
)

router = APIRouter(
    prefix="/claims",
    tags=["Claims"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "",
    response_model=ClaimResponse,
    #dependencies=[Depends(get_current_user)],
)
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


@router.get(
    "/{claim_id}",
    response_model=ClaimSummaryResponse,
    #dependencies=[Depends(get_current_user)],
)
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