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

        # 1. Create initial DB record
        claim = self.repository.get_claim(claim_id)

        if not claim:
            self.repository.create_claim(
                claim_id=claim_id,
                customer_id=state["customer_id"],
                customer_message=state["customer_message"],
            )

        # 2. Run LangGraph
        result = await self.claim_graph.ainvoke(state)

        # 3. Persist final result
        final_decision = None

        if result.get("final_claim"):
            final_decision = result.get("status")

        self.repository.update_claim(
            claim_id=claim_id,
            status=result.get("status", "PROCESSING"),
            claim_complete=result.get("claim_complete", False),
            final_decision=final_decision,
        )

        return result

    def get_claim(self, claim_id: str):
        return self.repository.get_claim(claim_id)
