from pydantic import BaseModel, Field
from datetime import datetime

class AccountBase(BaseModel):
    balance: float = Field(..., ge=0, description="Баланс счета", example=1000.50)

class AccountCreate(AccountBase):
    user_id: int = Field(..., description="ID владельца счета")

class AccountInDB(AccountBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True