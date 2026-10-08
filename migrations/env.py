"""Alembic runs this file. It migrates the database named by PAYMENTS_DATABASE_URL."""

from alembic import context
from sqlalchemy import create_engine

import payments.models  # noqa: F401  (registers the tables on Base.metadata)
from payments import settings
from payments.db import Base

engine = create_engine(settings.DATABASE_URL)
with engine.connect() as connection:
    context.configure(connection=connection, target_metadata=Base.metadata, render_as_batch=True)
    with context.begin_transaction():
        context.run_migrations()
