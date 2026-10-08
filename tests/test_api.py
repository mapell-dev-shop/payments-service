from fastapi.testclient import TestClient
from shop_contracts.messaging import InMemoryEventPublisher
from sqlalchemy.orm import Session

from payments.handlers import handle_stock_reserved
from tests.conftest import event


def test_a_payment_can_be_read_by_order_id(
    client: TestClient, session: Session, publisher: InMemoryEventPublisher
) -> None:
    handle_stock_reserved(
        session, event("StockReserved", {"order_id": "o-1", "total_cents": 5000}), publisher
    )

    response = client.get("/payments/o-1")

    assert response.status_code == 200
    assert response.json()["status"] == "CAPTURED"


def test_no_payment_for_an_order_gives_404(client: TestClient) -> None:
    assert client.get("/payments/o-unknown").status_code == 404
