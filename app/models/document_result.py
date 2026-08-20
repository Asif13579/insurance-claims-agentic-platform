from typing import Any, Optional

from pydantic import BaseModel, Field


class DocumentExtraction(BaseModel):
    """
    Structured information extracted from a document.
    """

    incident_type: Optional[str] = None
    incident_date: Optional[str] = None
    incident_location: Optional[str] = None

    estimated_amount: Optional[float] = None

    vehicle: Optional[str] = None

    hospital_name: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None

    additional_data: dict[str, Any] = Field(default_factory=dict)


class DocumentResult(BaseModel):
    """
    Result produced by the document intelligence agent.
    """

    filename: str
    document_type: str

    valid: bool = True

    extraction: Optional[DocumentExtraction] = None

    errors: list[str] = Field(default_factory=list)
