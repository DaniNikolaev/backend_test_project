import hashlib
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.payment import PaymentCreate, PaymentInDB
from app.crud.payment import payment_crud
from app.dependencies import get_db
from app.services.config import settings

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/webhook", response_model=PaymentInDB)
def payment_webhook(
    payment: PaymentCreate,
    db: Session = Depends(get_db)
):
    # Валидация подписи
    data = payment.dict()
    sorted_data = sorted(data.items(), key=lambda x: x[0])
    signature_str = ''.join(str(v) for k, v in sorted_data if k != 'signature')
    signature_str += settings.SECRET_KEY
    calculated_signature = hashlib.sha256(signature_str.encode()).hexdigest()

    if calculated_signature != payment.signature:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Обработка платежа
    result = payment_crud.process_payment_sync(db, payment)
    if not result:
        raise HTTPException(status_code=400, detail="Payment already processed")

    return result
