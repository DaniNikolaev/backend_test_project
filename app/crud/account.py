from typing import Any, Sequence, Type
from sqlalchemy.orm import Session
from sqlalchemy import select, Row, RowMapping
from app.models.account import Account


class AccountCRUD:
    def create_for_user(self, db: Session, user_id: int) -> Account:
        """Создает счет для пользователя"""
        account = Account(user_id=user_id, balance=0.0)
        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    def get_by_user(self, db: Session, user_id: int) -> Sequence[Row | RowMapping | Any]:
        """Получает все счета пользователя"""
        result = db.execute(select(Account).filter(Account.user_id == user_id))
        return result.scalars().all()

    def update_balance(
        self,
        db: Session,
        account_id: int,
        amount: float
    ) -> Type[Account] | None:
        """Обновляет баланс счета"""
        account = db.get(Account, account_id)
        if not account:
            return None
        account.balance += amount
        db.commit()
        db.refresh(account)
        return account


account_crud = AccountCRUD()
