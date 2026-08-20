from typing import TypedDict, List, Dict, Any, Optional


class ClaimState(TypedDict, total=False):
    # --------------------------------------------------
    # Customer / claim input
    # --------------------------------------------------

    claim_id: str
    customer_id: str
    customer_message: str

    # --------------------------------------------------
    # Intake / extracted customer information
    # --------------------------------------------------

    customer_data: Dict[str, Any]

    accident_date: Optional[str]
    accident_description: Optional[str]
    accident_location: Optional[str]

    # --------------------------------------------------
    # Documents supplied by customer
    # --------------------------------------------------

    documents: List[Dict[str, Any]]

    # --------------------------------------------------
    # Document validation
    # --------------------------------------------------

    valid_documents: List[Dict[str, Any]]
    invalid_documents: List[Dict[str, Any]]
    missing_documents: List[str]

    # --------------------------------------------------
    # Document intelligence
    # --------------------------------------------------

    document_results: List[Dict[str, Any]]
    extracted_data: Dict[str, Any]

    # --------------------------------------------------
    # Consistency validation
    # --------------------------------------------------

    consistency_check: Dict[str, Any]
    consistency_issues: List[Dict[str, Any]]

    # --------------------------------------------------
    # Claim decision
    # --------------------------------------------------

    claim_decision: Dict[str, Any]

    # --------------------------------------------------
    # Manual review
    # --------------------------------------------------

    review: Dict[str, Any]

    # --------------------------------------------------
    # Final decision / response
    # --------------------------------------------------

    final_response: Dict[str, Any]

    # --------------------------------------------------
    # Workflow status
    # --------------------------------------------------

    status: str
    claim_complete: bool

    # --------------------------------------------------
    # Customer-facing message
    # --------------------------------------------------

    customer_message_response: Optional[str]

    # --------------------------------------------------
    # Final claim package
    # --------------------------------------------------

    final_claim: Optional[Dict[str, Any]]