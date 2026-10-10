# payments-service

The payments bounded context of the shop. It charges orders through a fake gateway that declines any amount above 1000.00, so the demo has a failure path.

## Run it

`./run-all.sh` in the shop workspace starts it with everything else. On its own:

    uv sync
    uv run alembic upgrade head
    uv run uvicorn payments.api:app --port 8003
    uv run python -m payments.worker

## Test it

    uv run pytest
    uv run ruff check . && uv run ruff format --check .
    uv run mypy src

## Events

* Consumes `StockReserved` and `OrderCancelled`.
* Publishes `PaymentCaptured` or `PaymentFailed`.
* On `OrderCancelled`, a `CAPTURED` payment becomes `REFUNDED` and `PaymentRefunded` is published. Cancelling again publishes `PaymentRefunded` again.
* A `StockReserved` for a cancelled order captures nothing.

## Known limitations

* The event is published after the database commit. If publishing fails or the process dies in between, the payment exists and nobody hears about it. A failed publish stops the worker with an error.
* Run one worker at a time. A late `StockReserved` is refused only because the worker handles `OrderCancelled` and `StockReserved` one after the other.
* A lost `PaymentRefunded` is published again when the customer cancels the order again.
* Out of scope for cancelling: inventory overselling under concurrent reservations, authentication on cancel, cancelling part of an order, failing refunds, and a cutoff after which an order can no longer be cancelled.
