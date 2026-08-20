from typing import List

from pydantic import BaseModel


class DocumentRequest(BaseModel):
    filename: str
    document_type: str


class ClaimRequest(BaseModel):
    claim_id: str
    customer_id: str
    customer_message: str
    documents: List[DocumentRequest]


class ClaimProcessRequest(BaseModel):
    claim_id: str
    customer_id: str
    customer_message: str
    documents: List[DocumentRequest]