from enum import StrEnum

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from payments.db import Base


class PaymentStatus(StrEnum):
    CAPTURED = "CAPTURED"
    FAILED = "FAILED"


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = (UniqueConstraint("order_id", name="uq_payments_order_id"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    order_id: Mapped[str] = mapped_column(String(36))
    amount_cents: Mapped[int]
    status: Mapped[str] = mapped_column(String(20))


class ProcessedEvent(Base):
    """Ids of events already handled, so a redelivered event changes nothing."""

    __tablename__ = "processed_events"

    event_id: Mapped[str] = mapped_column(String(36), primary_key=True)
