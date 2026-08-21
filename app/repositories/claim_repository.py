from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.claim import Claim


class ClaimRepository:

    def __init__(self, db: Session):
        self.db = db

    # -----------------------------------------
    # Create
    # -----------------------------------------

    def create_claim(
        self,
        claim_id: str,
        customer_id: str,
        customer_message: str,
    ):
        claim = Claim(
            claim_id=claim_id,
            customer_id=customer_id,
            customer_message=customer_message,
            status="RECEIVED",
        )

        self.db.add(claim)

        try:
            self.db.commit()
            self.db.refresh(claim)
            return claim

        except IntegrityError:
            self.db.rollback()
            raise

    # -----------------------------------------
    # Get
    # -----------------------------------------

    def get_claim(self, claim_id: str):
        return (
            self.db.query(Claim)
            .filter(Claim.claim_id == claim_id)
            .first()
        )

    # -----------------------------------------
    # Update
    # -----------------------------------------

    def update_claim(
        self,
        claim_id: str,
        status: str,
        claim_complete: bool,
        final_decision: str | None = None,
    ):
        claim = self.get_claim(claim_id)

        if not claim:
            return None

        claim.status = status
        claim.claim_complete = str(claim_complete).lower()

        if final_decision is not None:
            claim.final_decision = final_decision

        try:
            self.db.commit()
            self.db.refresh(claim)
            return claim

        except SQLAlchemyError:
            self.db.rollback()
            raise