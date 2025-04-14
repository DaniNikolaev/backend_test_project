from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from app.crud.user import user_crud
from app.models import User
from app.services.config import settings
from app.services.database import get_db  # Импортируем исправленную функцию

# Настройка OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_db_session() -> Session:
    """
    Зависимость для получения сессии БД.
    Теперь возвращает непосредственно объект сессии, а не генератор.
    """
    return get_db()  # Используем исправленную функцию из database.py


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e

    user = user_crud.get_by_email(get_db_session(), email=email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_admin(
        current_user: User = Depends(get_current_user)
) -> User:
    """
    Проверка прав администратора.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user


# Аннотированные типы для удобного использования в роутерах
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentAdmin = Annotated[User, Depends(get_current_admin)]
CurrentDBSession = Annotated[Session, Depends(get_db_session)]
