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

* Consumes `StockReserved`.
* Publishes `PaymentCaptured` or `PaymentFailed`.

## Known limitations

* The event is published after the database commit. If publishing fails or the process dies in between, the payment exists and nobody hears about it. A failed publish stops the worker with an error.
