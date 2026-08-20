class DecisionAgent:

    async def process(self, state):

        claim_decision = state.get("claim_decision")

        # Missing decision
        if not claim_decision:
            state["final_response"] = {
                "status": "error",
                "message": "Claim decision is unavailable.",
            }
            return state

        decision = claim_decision.get("decision")
        reason = claim_decision.get("reason", "")

        # Approved
        if decision == "APPROVE":
            state["final_response"] = {
                "status": "approved",
                "message": "Your claim has been approved.",
                "reason": reason,
            }
            return state

        # Documents required
        if decision == "REQUEST_MORE_INFORMATION":
            state["final_response"] = {
                "status": "documents_required",
                "message": "Additional documents are required.",
                "reason": reason,
                "missing_documents": claim_decision.get(
                    "missing_documents",
                    []
                ),
            }
            return state

        # Manual review
        if decision == "MANUAL_REVIEW":
            state["final_response"] = {
                "status": "manual_review",
                "message": "Your claim requires manual review.",
                "reason": reason,
            }
            return state

        # Unknown decision
        state["final_response"] = {
            "status": "error",
            "message": "Claim decision is unavailable.",
            "reason": reason,
        }

        return state
