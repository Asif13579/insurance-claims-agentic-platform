from typing import TypedDict, List, Dict, Any, Optional

class ClaimState(TypedDict, total=False):
    # Customer input
    claim_id: str
    customer_id: str
    customer_message: str

    # Documents supplied by customer
    documents: List[Dict[str, Any]]

    # Information extracted from customer message
    accident_date: Optional[str]
    accident_description: Optional[str]
    accident_location: Optional[str]

    # Document processing
    valid_documents: List[Dict[str, Any]]
    invalid_documents: List[Dict[str, Any]]
    missing_documents: List[str]

    # Consistency checks
    consistency_issues: List[Dict[str, Any]]

    # Final workflow status
    status: str
    claim_complete: bool

    # Customer-facing message
    customer_message_response: Optional[str]

    # Final claim package
    final_claim: Optional[Dict[str, Any]]

# class ClaimDocument(TypedDict, total=False):
#     filename: str
#     document_type: str
#     content: str
#     status: str

# class DocumentResult(TypedDict, total=False):
#     filename: str
#     document_type: str
#     valid: bool
#     status: str
#     message: str

# class ConsistencyResult(TypedDict, total=False):
#     consistent: bool
#     issues: List[str]
#     message: str

# class ClaimDecision(TypedDict, total=False):
#     decision: str
#     reason: str
#     confidence: float

# class ClaimState(TypedDict, total=False):
#     claim_id: str
#     customer_id: str
#     customer_message: str

#     documents: List[ClaimDocument]
#     document_results: List[DocumentResult]

#     consistency_results: ConsistencyResult

#     claim_decision: ClaimDecision

#     status: str

    