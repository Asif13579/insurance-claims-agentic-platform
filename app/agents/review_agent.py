class ReviewAgent:

    async def process(self, state):

        consistency_check = state.get("consistency_check")

        # Missing consistency information
        if not consistency_check:
            state["status"] = "NEEDS_REVIEW"
            state["claim_complete"] = False

            state["review"] = {
                "required": True,
                "status": "pending",
                "reason": "Consistency check is missing.",
                "recommended_action": "manual_review",
            }

            state["claim_decision"] = {
                "decision": "MANUAL_REVIEW",
                "reason": "Consistency check is missing.",
            }

            return state

        # Inconsistent claim
        if consistency_check.get("consistent") is False:

            reason = consistency_check.get(
                "reason",
                "Claim contains inconsistent information.",
            )

            state["status"] = "NEEDS_REVIEW"
            state["claim_complete"] = False

            state["review"] = {
                "required": True,
                "status": "pending",
                "reason": reason,
                "recommended_action": "manual_review",
            }

            state["claim_decision"] = {
                "decision": "MANUAL_REVIEW",
                "reason": reason,
            }

            return state

        # Consistent claim
        state["review"] = {
            "required": False,
            "status": "not_required",
            "reason": "Claim is consistent.",
            "recommended_action": "continue",
        }

        return state
