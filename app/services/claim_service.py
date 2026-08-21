from fastapi import HTTPException

from app.models.claim_state import ClaimState
from app.repositories.claim_repository import ClaimRepository
from app.graph.workflow import build_claim_graph
from app.core.logging import get_logger


logger = get_logger("claim.service")


class ClaimService:

    def __init__(self, db):
        self.db = db
        self.repository = ClaimRepository(db)
        self.claim_graph = build_claim_graph()

    async def process_claim(self, state: ClaimState):

        claim_id = state["claim_id"]

        logger.info(
            "claim_started claim_id=%s",
            claim_id,
        )

        # Reject duplicate claims before running the workflow
        existing_claim = self.repository.get_claim(claim_id)

        if existing_claim:
            logger.warning(
                "duplicate_claim claim_id=%s",
                claim_id,
            )

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

        logger.info(
            "claim_record_created claim_id=%s",
            claim_id,
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

        # Structured observability logging
        logger.info(
            "claim_completed claim_id=%s status=%s decision=%s",
            claim_id,
            result.get("status"),
            final_decision,
        )

        logger.info(
            "claim_workflow_summary claim_id=%s "
            "documents=%s review=%s",
            claim_id,
            len(result.get("document_results", [])),
            bool(result.get("review")),
        )

        return result

    def get_claim(self, claim_id: str):
        return self.repository.get_claim(claim_id)