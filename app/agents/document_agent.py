from app.models.claim_state import ClaimState


class DocumentAgent:

    REQUIRED_DOCUMENTS = {
        "police_report",
        "repair_estimate",
        "photo",
    }

    async def process(self, state: ClaimState) -> ClaimState:

        documents = state.get("documents", [])

        valid_documents = []
        invalid_documents = []

        # -----------------------------------------
        # Validate submitted documents
        # -----------------------------------------

        for document in documents:

            # Support both:
            # 1. dict
            # 2. Pydantic DocumentRequest
            if isinstance(document, dict):
                filename = document.get("filename")
                document_type = document.get("document_type")
            else:
                filename = getattr(document, "filename", None)
                document_type = getattr(document, "document_type", None)

            # Missing filename or document type
            if not filename or not document_type:

                invalid_documents.append({
                    "filename": filename,
                    "document_type": document_type,
                    "reason": "Missing filename or document type"
                })

                continue

            # Unsupported document type
            if document_type not in self.REQUIRED_DOCUMENTS:

                invalid_documents.append({
                    "filename": filename,
                    "document_type": document_type,
                    "reason": "Unsupported document type"
                })

                continue
            # Store normalized dictionary
            valid_document = {
                "filename": filename,
                "document_type": document_type,
            }

            if isinstance(document, dict) and "content" in document:
                valid_document["content"] = document["content"]

            valid_documents.append(valid_document)
            # Store normalized dictionary
            # valid_documents.append({
            #     "filename": filename,
            #     "document_type": document_type
            # })

            

        # -----------------------------------------
        # Determine missing documents
        # -----------------------------------------

        submitted_types = {
            document["document_type"]
            for document in valid_documents
        }

        missing_documents = sorted(
            self.REQUIRED_DOCUMENTS - submitted_types
        )

        # -----------------------------------------
        # Update ClaimState
        # -----------------------------------------

        state["valid_documents"] = valid_documents
        state["invalid_documents"] = invalid_documents
        state["missing_documents"] = missing_documents

        # -----------------------------------------
        # Determine status
        # -----------------------------------------

        if missing_documents or invalid_documents:
            state["status"] = "NEEDS_DOCUMENTS"
        else:
            state["status"] = "DOCUMENTS_REVIEWED"

        return state
