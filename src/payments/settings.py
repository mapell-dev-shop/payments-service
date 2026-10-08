import os

DATABASE_URL = os.environ.get("PAYMENTS_DATABASE_URL", "sqlite:///payments.db")
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
