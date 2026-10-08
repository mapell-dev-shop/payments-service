from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from payments.db import get_session
from payments.models import Payment

app = FastAPI(title="payments-service")


class PaymentOut(BaseModel):
    id: str
    order_id: str
    amount_cents: int
    status: str


@app.get("/payments/{order_id}")
def get_payment(order_id: str, session: Annotated[Session, Depends(get_session)]) -> PaymentOut:
    payment = session.scalar(select(Payment).where(Payment.order_id == order_id))
    if payment is None:
        raise HTTPException(404, "payment not found")
    return PaymentOut(
        id=payment.id,
        order_id=payment.order_id,
        amount_cents=payment.amount_cents,
        status=payment.status,
    )
