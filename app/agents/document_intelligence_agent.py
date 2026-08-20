from app.models.claim_state import ClaimState
from app.models.document_result import (
    DocumentExtraction,
    DocumentResult,
)


class DocumentIntelligenceAgent:
    """
    Phase 7 document intelligence agent.

    Currently provides deterministic document processing.
    Real PDF parsing, OCR, image validation, and LLM extraction
    can be added later without changing the ClaimState contract.
    """

    SUPPORTED_DOCUMENT_TYPES = {
        "police_report",
        "repair_estimate",
        "photo",
    }

    async def process(self, state: ClaimState) -> ClaimState:

        documents = state.get("valid_documents", [])

        document_results = []
        extracted_data = {}

        for document in documents:

            filename = document.get("filename")
            document_type = document.get("document_type")

            # -----------------------------------------
            # Validate document metadata
            # -----------------------------------------

            if not filename or not document_type:

                result = DocumentResult(
                    filename=filename or "",
                    document_type=document_type or "",
                    valid=False,
                    errors=[
                        "Missing filename or document type"
                    ],
                )

                document_results.append(result.model_dump())
                continue

            # -----------------------------------------
            # Check supported document type
            # -----------------------------------------

            if document_type not in self.SUPPORTED_DOCUMENT_TYPES:

                result = DocumentResult(
                    filename=filename,
                    document_type=document_type,
                    valid=False,
                    errors=[
                        "Unsupported document type"
                    ],
                )

                document_results.append(result.model_dump())
                continue

            # -----------------------------------------
            # Deterministic extraction
            #
            # Real extraction will be added later.
            # -----------------------------------------

            extraction = DocumentExtraction()

            result = DocumentResult(
                filename=filename,
                document_type=document_type,
                valid=True,
                extraction=extraction,
            )

            document_results.append(result.model_dump())

            extracted_data[document_type] = (
                extraction.model_dump()
            )

        # -----------------------------------------
        # Update ClaimState
        # -----------------------------------------

        state["document_results"] = document_results
        state["extracted_data"] = extracted_data

        return state
