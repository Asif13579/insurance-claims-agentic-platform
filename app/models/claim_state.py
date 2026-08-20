from typing import TypedDict


class ClaimState(TypedDict, total=False):

    # -----------------------------------------
    # Claim identity
    # -----------------------------------------

    claim_id: str
    customer_id: str
    customer_message: str

    # -----------------------------------------
    # Phase 6 - Intake
    # -----------------------------------------

    customer_data: dict

    # -----------------------------------------
    # Phase 7 - Document intelligence
    # -----------------------------------------

    documents: list
    valid_documents: list
    invalid_documents: list
    missing_documents: list

    document_results: list
    extracted_data: dict

    # -----------------------------------------
    # Phase 8 - Consistency
    # -----------------------------------------

    consistency_check: dict
    consistency_results: dict
    inconsistencies: list
    questions: list

    # -----------------------------------------
    # Review
    # -----------------------------------------

    review: dict

    # -----------------------------------------
    # Final decision
    # -----------------------------------------

    claim_decision: dict
    final_response: dict
    final_claim: dict

    # -----------------------------------------
    # Workflow
    # -----------------------------------------

    status: str
    claim_complete: bool
