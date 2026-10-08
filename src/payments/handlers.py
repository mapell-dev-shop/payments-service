"""What payments-service does when an event arrives from another service."""

import uuid
from typing import Any

from shop_contracts.events import new_envelope
from shop_contracts.messaging import EventPublisher
from sqlalchemy.orm import Session

from payments.models import Payment, PaymentStatus, ProcessedEvent

# The fake gateway declines anything above this amount, so the demo has a failure path.
CAPTURE_LIMIT_CENTS = 100_000


def handle_stock_reserved(
    session: Session, envelope: dict[str, Any], publisher: EventPublisher
) -> None:
    if session.get(ProcessedEvent, envelope["event_id"]) is not None:
        return
    order_id = envelope["data"]["order_id"]
    amount = envelope["data"]["total_cents"]
    captured = amount <= CAPTURE_LIMIT_CENTS
    payment = Payment(
        id=str(uuid.uuid4()),
        order_id=order_id,
        amount_cents=amount,
        status=PaymentStatus.CAPTURED if captured else PaymentStatus.FAILED,
    )
    session.add(payment)
    session.add(ProcessedEvent(event_id=envelope["event_id"]))
    session.commit()

    if captured:
        result = new_envelope(
            "PaymentCaptured",
            {"order_id": order_id, "payment_id": payment.id, "amount_cents": amount},
        )
    else:
        result = new_envelope(
            "PaymentFailed", {"order_id": order_id, "reason": "amount over limit"}
        )
    publisher.publish(result, key=order_id)
