from shop_contracts.messaging import InMemoryEventPublisher
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from payments.handlers import CAPTURE_LIMIT_CENTS, handle_stock_reserved
from payments.models import Payment
from tests.conftest import event


def stock_reserved(total_cents: int) -> dict[str, object]:
    return event("StockReserved", {"order_id": "o-1", "total_cents": total_cents})


def test_an_amount_within_the_limit_is_captured(
    session: Session, publisher: InMemoryEventPublisher
) -> None:
    handle_stock_reserved(session, stock_reserved(5000), publisher)

    payment = session.scalar(select(Payment))
    assert payment is not None and payment.status == "CAPTURED"
    [envelope] = publisher.published
    assert envelope["type"] == "PaymentCaptured"
    assert envelope["data"] == {"order_id": "o-1", "payment_id": payment.id, "amount_cents": 5000}


def test_exactly_the_limit_is_still_captured(
    session: Session, publisher: InMemoryEventPublisher
) -> None:
    handle_stock_reserved(session, stock_reserved(CAPTURE_LIMIT_CENTS), publisher)

    assert publisher.published[0]["type"] == "PaymentCaptured"


def test_an_amount_over_the_limit_fails(
    session: Session, publisher: InMemoryEventPublisher
) -> None:
    handle_stock_reserved(session, stock_reserved(CAPTURE_LIMIT_CENTS + 1), publisher)

    payment = session.scalar(select(Payment))
    assert payment is not None and payment.status == "FAILED"
    [envelope] = publisher.published
    assert envelope["data"] == {"order_id": "o-1", "reason": "amount over limit"}


def test_a_redelivered_event_charges_once(
    session: Session, publisher: InMemoryEventPublisher
) -> None:
    envelope = stock_reserved(5000)

    handle_stock_reserved(session, envelope, publisher)
    handle_stock_reserved(session, envelope, publisher)

    assert session.scalar(select(func.count()).select_from(Payment)) == 1
    assert len(publisher.published) == 1
