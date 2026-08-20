from app.models.claim_state import ClaimState


class ConsistencyAgent:

    REQUIRED_DOCUMENTS = {
        "police_report",
        "repair_estimate",
        "photo",
    }

    async def process(self, state: ClaimState) -> ClaimState:

        documents = state.get("documents", [])

        document_types = set()

        for document in documents:
            if isinstance(document, dict):
                document_type = document.get("document_type")
            else:
                document_type = getattr(
                    document,
                    "document_type",
                    None
                )

            if document_type:
                document_types.add(document_type)

        issues = []

        # -----------------------------------------
        # Missing required documents
        # -----------------------------------------

        missing = self.REQUIRED_DOCUMENTS - document_types

        if missing:
            issues.append(
                f"Missing required documents: "
                f"{', '.join(sorted(missing))}"
            )

        # -----------------------------------------
        # Unexpected documents
        # -----------------------------------------

        unexpected = document_types - self.REQUIRED_DOCUMENTS

        if unexpected:
            issues.append(
                f"Unexpected document types: "
                f"{', '.join(sorted(unexpected))}"
            )

        # -----------------------------------------
        # Invalid documents from DocumentAgent
        # -----------------------------------------

        invalid_documents = state.get(
            "invalid_documents",
            []
        )

        if invalid_documents:
            for document in invalid_documents:
                filename = document.get("filename", "")
                reason = document.get(
                    "reason",
                    "Invalid document"
                )

                issues.append(
                    f"{filename}: {reason}"
                )

        # -----------------------------------------
        # Determine consistency
        # -----------------------------------------

        consistent = len(issues) == 0

        reason = (
            "Claim documents are consistent."
            if consistent
            else "; ".join(issues)
        )

        state["consistency_check"] = {
            "consistent": consistent,
            "issues": issues,
            "reason": reason,
        }

        return state
