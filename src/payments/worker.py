"""Kafka consumer process of payments-service: python -m payments.worker"""

from typing import Any

from shop_contracts.messaging import KafkaEventPublisher, run_consumer

from payments import settings
from payments.db import SessionLocal
from payments.handlers import handle_stock_reserved


def main() -> None:
    publisher = KafkaEventPublisher(settings.KAFKA_BOOTSTRAP_SERVERS)

    def on_stock_reserved(envelope: dict[str, Any]) -> None:
        with SessionLocal() as session:
            handle_stock_reserved(session, envelope, publisher)

    run_consumer(
        settings.KAFKA_BOOTSTRAP_SERVERS, "payments-service", {"StockReserved": on_stock_reserved}
    )


if __name__ == "__main__":
    main()
