# Импорт всех моделей
from .base import Base
from .user import User
from .account import Account
from .payment import Payment

# Явное указание всех моделей для Alembic
__all__ = [
    'Base',
    'User',
    'Account',
    'Payment'
]