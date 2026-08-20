from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text
from app.config.database import Base


class Claim(Base):
    __tablename__ = "claims"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    claim_id = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    customer_id = Column(
        String(50),
        nullable=False
    )

    customer_message = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(50),
        nullable=False,
        default="RECEIVED"
    )

    claim_complete = Column(
        String(10),
        nullable=False,
        default="false"
    )

    final_decision = Column(
        String(100),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )