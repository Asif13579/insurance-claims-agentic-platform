from typing import Any, List, Optional

from pydantic import BaseModel, Field


class DocumentResponse(BaseModel):
    filename: str
    document_type: str


class CustomerDataResponse(BaseModel):
    incident_type: Optional[str] = None
    incident_date: Optional[str] = None
    incident_location: Optional[str] = None
    hospitalized: Optional[bool] = None
    hospital_name: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    estimated_amount: Optional[float] = None
    description: Optional[str] = None


class DocumentExtractionResponse(BaseModel):
    incident_type: Optional[str] = None
    incident_date: Optional[str] = None
    incident_location: Optional[str] = None
    estimated_amount: Optional[float] = None
    vehicle: Optional[str] = None
    hospital_name: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    #additional_data: dict[str, Any] = {}
    additional_data: dict[str, Any] = Field(default_factory=dict)


class DocumentResultResponse(BaseModel):
    filename: str
    document_type: str
    valid: bool
    extraction: DocumentExtractionResponse
    errors: List[str]


class ConsistencyCheckResponse(BaseModel):
    consistent: bool
    issues: List[str]
    reason: str


class ReviewResponse(BaseModel):
    required: bool
    status: str
    reason: str
    recommended_action: str


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

    customer_data: CustomerDataResponse

    documents: List[DocumentResponse]
    valid_documents: List[DocumentResponse]
    invalid_documents: List[DocumentResponse]
    missing_documents: List[str]

    document_results: List[DocumentResultResponse]
    extracted_data: dict[str, DocumentExtractionResponse]

    consistency_check: Optional[ConsistencyCheckResponse] = None
    inconsistencies: List[str]

    review: Optional[ReviewResponse] = None

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