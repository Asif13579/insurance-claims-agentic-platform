class DecisionAgent:

    async def process(self, state):

        claim_decision = state.get("claim_decision")
        if claim_decision:
            final_decision = claim_decision.get("decision")
        
        # -----------------------------------------
        # Missing decision
        # -----------------------------------------

        if not claim_decision:

            state["status"] = "ERROR"
            state["claim_complete"] = False

            state["final_response"] = {
                "status": "error",
                "message": "Claim decision is unavailable.",
            }

            return state

        decision = claim_decision.get("decision")
        reason = claim_decision.get("reason", "")

        # -----------------------------------------
        # Approved
        # -----------------------------------------

        if decision == "APPROVE":

            state["status"] = "APPROVED"
            state["claim_complete"] = True

            state["final_response"] = {
                "status": "approved",
                "message": "Your claim has been approved.",
                "reason": reason,
            }

            return state

        # -----------------------------------------
        # More documents required
        # -----------------------------------------

        if decision == "REQUEST_MORE_INFORMATION":

            state["status"] = "NEEDS_DOCUMENTS"
            state["claim_complete"] = False

            state["final_response"] = {
                "status": "documents_required",
                "message": "Additional documents are required.",
                "reason": reason,
                "missing_documents": claim_decision.get(
                    "missing_documents",
                    [],
                ),
            }

            return state

        # -----------------------------------------
        # Manual review
        # -----------------------------------------

        if decision == "MANUAL_REVIEW":

            state["status"] = "NEEDS_REVIEW"
            state["claim_complete"] = False

            state["final_response"] = {
                "status": "manual_review",
                "message": "Your claim requires manual review.",
                "reason": reason,
            }

            return state

        # -----------------------------------------
        # Unknown decision
        # -----------------------------------------

        state["status"] = "ERROR"
        state["claim_complete"] = False

        state["final_response"] = {
            "status": "error",
            "message": "Claim decision is unavailable.",
            "reason": reason,
        }

        return state