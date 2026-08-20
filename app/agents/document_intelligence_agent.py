from app.models.claim_state import ClaimState
from app.models.document_result import (
    DocumentExtraction,
    DocumentResult,
)


class DocumentIntelligenceAgent:
    """
    Document intelligence agent.

    Uses deterministic extraction when no LLM is provided.
    Uses structured LLM extraction when an LLM is provided.
    """

    SUPPORTED_DOCUMENT_TYPES = {
        "police_report",
        "repair_estimate",
        "photo",
    }

    def __init__(self, llm=None):
        self.llm = llm

    async def process(
        self,
        state: ClaimState
    ) -> ClaimState:

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

                document_results.append(
                    result.model_dump()
                )

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

                document_results.append(
                    result.model_dump()
                )

                continue

            # -----------------------------------------
            # Extract document content
            # -----------------------------------------

            document_content = document.get(
                "content",
                ""
            )

            # -----------------------------------------
            # Deterministic fallback
            # -----------------------------------------

            if self.llm is None:

                extraction = DocumentExtraction()

            # -----------------------------------------
            # LLM structured extraction
            # -----------------------------------------

            else:

                structured_llm = (
                    self.llm.with_structured_output(
                        DocumentExtraction
                    )
                )

                system_prompt = """
You are an insurance document intelligence agent.

Your task is to extract factual information from
the provided insurance claim document.

Extraction rules:

- Extract only information explicitly present
  in the document.
- Never invent information.
- If a field is not present, return null.
- Preserve dates exactly as stated.
- Extract estimated amounts only when explicitly
  stated.
- Extract vehicle information only when explicitly
  stated.
- Extract hospital, diagnosis, and treatment only
  when explicitly stated.
- Put document-specific information that does not
  fit the schema into additional_data.
"""

                user_prompt = f"""
Document filename:
{filename}

Document type:
{document_type}

Document content:

{document_content}
"""

                extraction = await structured_llm.ainvoke(
                    [
                        ("system", system_prompt),
                        ("human", user_prompt),
                    ]
                )

            # -----------------------------------------
            # Build document result
            # -----------------------------------------

            result = DocumentResult(
                filename=filename,
                document_type=document_type,
                valid=True,
                extraction=extraction,
            )

            document_results.append(
                result.model_dump()
            )

            extracted_data[document_type] = (
                extraction.model_dump()
            )

        # -----------------------------------------
        # Update ClaimState
        # -----------------------------------------

        state["document_results"] = document_results
        state["extracted_data"] = extracted_data

        return state