from pydantic import BaseModel, Field


class AccountBase(BaseModel):
    balance: float = Field(..., ge=0, description="Баланс счета", example=1000.50)


class AccountCreate(AccountBase):
    user_id: int = Field(..., description="ID владельца счета")


class AccountInDB(AccountBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
