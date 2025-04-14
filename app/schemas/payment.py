from datetime import datetime
from pydantic import BaseModel, Field, UUID4


class PaymentBase(BaseModel):
    amount: float = Field(..., gt=0, description="Сумма платежа", example=150.75)
    transaction_id: UUID4 = Field(..., description="Уникальный ID транзакции")
    account_id: int = Field(..., description="ID счета")
    user_id: int = Field(..., description="ID пользователя")


class PaymentCreate(PaymentBase):
    signature: str = Field(..., description="Подпись транзакции")


class PaymentInDB(PaymentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
