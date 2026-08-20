from typing import List, Optional

from pydantic import BaseModel


class ClaimDecisionResponse(BaseModel):
    decision: str
    reason: str
    missing_documents: Optional[List[str]] = None


class FinalResponse(BaseModel):
    status: str
    message: str
    reason: Optional[str] = None
    missing_documents: Optional[List[str]] = None


class ClaimResponse(BaseModel):
    claim_id: str
    customer_id: str
    customer_message: str

    customer_data: dict

    documents: List[dict]
    valid_documents: List[dict]
    invalid_documents: List[dict]
    missing_documents: List[str]

    document_results: List[dict]
    extracted_data: dict

    consistency_check: Optional[dict] = None
    inconsistencies: List[str]

    review: Optional[dict] = None

    claim_decision: ClaimDecisionResponse
    final_response: FinalResponse

    status: str
    claim_complete: bool


class ClaimSummaryResponse(BaseModel):
    claim_id: str
    customer_id: str
    status: str
    claim_complete: bool
    final_decision: Optional[str] = None