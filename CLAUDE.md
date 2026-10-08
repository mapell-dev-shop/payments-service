# payments-service

Owns payments. The map of the whole shop is in ../CLAUDE.md.

* Check your work with `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .` and `uv run mypy src`.
* The fake gateway declines amounts above `CAPTURE_LIMIT_CENTS` (1000.00). Keep it deterministic: the tests and the demo rely on it.
* One payment per order. `order_id` is unique in the database, and handled event ids are recorded in `processed_events`.
* A schema change is a new Alembic migration in `migrations/versions/`. Never edit a migration that has been applied.
* An event change starts in ../contracts (see its VERSIONING.md), never here.
