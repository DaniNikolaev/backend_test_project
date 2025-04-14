from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None  # Убрали example


class UserCreate(UserBase):
    password: str
    is_admin: bool = False
    is_active: bool = True  # Новые пользователи по умолчанию активны


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDB(UserBase):
    id: int
    is_admin: bool
    is_active: bool

    class Config:
        from_attributes = True  # Для работы с ORM
