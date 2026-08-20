class ClaimAgent:

    REQUIRED_DOCUMENTS = {
        "police_report",
        "repair_estimate",
        "photo",
    }

    async def process(self, state):

        consistency_check = state.get("consistency_check") or {}

        # -------------------------------------------------
        # Explicit consistency failure -> MANUAL_REVIEW
        # -------------------------------------------------

        if consistency_check.get("consistent") is False:

            # If the consistency failure is specifically caused
            # by missing documents, allow the missing-document
            # logic below to handle it.
            issues = consistency_check.get("issues", [])

            has_missing_documents_issue = any(
                "Missing required documents" in issue
                for issue in issues
            )

            if not has_missing_documents_issue:
                state["claim_decision"] = {
                    "decision": "MANUAL_REVIEW",
                    "reason": consistency_check.get(
                        "reason",
                        "Claim failed consistency validation.",
                    ),
                }

                return state

        # -------------------------------------------------
        # Prefer validated documents
        # -------------------------------------------------

        documents = state.get("valid_documents")

        if documents is None:
            documents = state.get("documents", [])

        submitted_types = {
            document.get("document_type")
            for document in documents
            if isinstance(document, dict)
        }

        # -------------------------------------------------
        # Check missing required documents
        # -------------------------------------------------

        missing_documents = sorted(
            self.REQUIRED_DOCUMENTS - submitted_types
        )

        if missing_documents:
            state["claim_decision"] = {
                "decision": "REQUEST_MORE_INFORMATION",
                "reason": "Required documents are missing.",
                "missing_documents": missing_documents,
            }

            return state

        # -------------------------------------------------
        # Invalid documents -> MANUAL_REVIEW
        # -------------------------------------------------

        invalid_documents = state.get(
            "invalid_documents",
            []
        )

        if invalid_documents:
            consistency_check = state.get(
                "consistency_check"
            ) or {}

            state["claim_decision"] = {
                "decision": "MANUAL_REVIEW",
                "reason": consistency_check.get(
                    "reason",
                    "Claim contains invalid documents.",
                ),
            }

            return state

        # -------------------------------------------------
        # Final consistency validation
        # -------------------------------------------------

        if consistency_check.get("consistent") is not True:

            state["claim_decision"] = {
                "decision": "MANUAL_REVIEW",
                "reason": consistency_check.get(
                    "reason",
                    "Claim failed consistency validation.",
                ),
            }

            return state

        # -------------------------------------------------
        # Approve
        # -------------------------------------------------

        state["claim_decision"] = {
            "decision": "APPROVE",
            "reason": (
                "Claim passed document and "
                "consistency validation."
            ),
        }

        return state
