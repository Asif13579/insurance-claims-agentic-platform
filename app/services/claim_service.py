from fastapi import HTTPException

from app.models.claim_state import ClaimState
from app.repositories.claim_repository import ClaimRepository
from app.graph.workflow import build_claim_graph


class ClaimService:

    def __init__(self, db):
        self.db = db
        self.repository = ClaimRepository(db)
        self.claim_graph = build_claim_graph()

    async def process_claim(self, state: ClaimState):

        claim_id = state["claim_id"]

        # Reject duplicate claims before running the workflow
        existing_claim = self.repository.get_claim(claim_id)

        if existing_claim:
            raise HTTPException(
                status_code=409,
                detail=f"Claim {claim_id} already exists",
            )

        # Create initial DB record
        self.repository.create_claim(
            claim_id=claim_id,
            customer_id=state["customer_id"],
            customer_message=state["customer_message"],
        )

        # Run LangGraph
        result = await self.claim_graph.ainvoke(state)

        # Persist final result
        final_decision = None

        claim_decision = result.get("claim_decision")

        if claim_decision:
            final_decision = claim_decision.get("decision")

        self.repository.update_claim(
            claim_id=claim_id,
            status=result.get("status", "PROCESSING"),
            claim_complete=result.get("claim_complete", False),
            final_decision=final_decision,
        )

        print("[SERVICE] Result keys:", sorted(result.keys()))
        print("[SERVICE] Claim decision:", result.get("claim_decision"))
        print("[SERVICE] Document results:", result.get("document_results"))
        print("[SERVICE] Review:", result.get("review"))
        print("[SERVICE] Final response:", result.get("final_response"))

        return result

    def get_claim(self, claim_id: str):
        return self.repository.get_claim(claim_id)