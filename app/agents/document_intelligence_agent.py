import re
from app.models.claim_state import ClaimState
from app.models.document_result import (
    DocumentExtraction,
    DocumentResult,
)
import time
from app.core.logging import get_logger
logger=get_logger("agent.document_intelligence")


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
    
    def _deterministic_extract(
        self,
        document_type: str,
        content: str,
    ) -> DocumentExtraction:

        text = content or ""

        def find(pattern: str):
            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE | re.MULTILINE,
            )
            return match.group(1).strip() if match else None

        incident_date = find(
            r"(?:incident date|accident date|date of accident)"
            r"\s*[:\-]\s*([^\r\n]+)"
        )

        incident_location = find(
            r"(?:incident location|accident location|location)"
            r"\s*[:\-]\s*([^\r\n]+)"
        )

        incident_type = find(
            r"(?:incident type|accident type|type of incident)"
            r"\s*[:\-]\s*([^\r\n]+)"
        )

        vehicle = find(
            r"(?:vehicle|car)"
            r"\s*[:\-]\s*([^\r\n]+)"
        )

        estimated_amount_text = find(
            r"(?:estimated repair cost|estimated amount|"
            r"repair estimate|total estimate)"
            r"\s*[:\-]?\s*(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d+)?)"
        )

        hospital_name = find(
            r"(?:hospital name|hospital)"
            r"\s*[:\-]\s*([^\r\n]+)"
        )

        diagnosis = find(
            r"(?:diagnosis|diagnosed with)"
            r"\s*[:\-]\s*([^\r\n]+)"
        )

        treatment = find(
            r"(?:treatment|treatment provided)"
            r"\s*[:\-]\s*([^\r\n]+)"
        )

        estimated_amount = None

        if estimated_amount_text:
            try:
                estimated_amount = float(
                    estimated_amount_text.replace(",", "")
                )
            except ValueError:
                estimated_amount = None

        return DocumentExtraction(
            incident_type=incident_type,
            incident_date=incident_date,
            incident_location=incident_location,
            estimated_amount=estimated_amount,
            vehicle=vehicle,
            hospital_name=hospital_name,
            diagnosis=diagnosis,
            treatment=treatment,
            additional_data={
                "extraction_method": "deterministic",
                "document_type": document_type,
            },
        )

    async def process(
        self,
        state: ClaimState
    ) -> ClaimState:
        start = time.perf_counter()
        documents = state.get("valid_documents", [])
        claim_id = state.get("claim_id","unknown",)
        logger.info("claim_id=%s agent=document_intelligence ""started documents=%d",claim_id,len(documents),)
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

                extraction = self._deterministic_extract(
                    document_type=document_type, content=document_content,
                )

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
        duration_ms = (
            time.perf_counter() - start
        ) * 1000

        logger.info(
            "claim_id=%s agent=document_intelligence "
            "completed extracted=%d duration_ms=%.2f",
            claim_id,
            len(extracted_data),
            duration_ms,
        )

        state["document_results"] = document_results
        state["extracted_data"] = extracted_data

        return state

    