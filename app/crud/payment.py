from typing import Any, Sequence
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, Row, RowMapping
from app.models.payment import Payment
from app.models.account import Account
from app.schemas import PaymentCreate


class PaymentCRUD:
    def create(
        self,
        db: Session,
        user_id: int,
        account_id: int,
        amount: float,
        transaction_id: UUID
    ) -> Payment:
        """Создает запись о платеже (для вебхука)"""
        payment = Payment(
            user_id=user_id,
            account_id=account_id,
            amount=amount,
            transaction_id=transaction_id
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    def get_by_transaction(
        self,
        db: Session,
        transaction_id: UUID
    ) -> Payment | None:
        """Проверяет дубликаты платежей"""
        result = db.execute(
            select(Payment).filter(Payment.transaction_id == transaction_id)
        )
        return result.scalars().first()

    def get_by_user(
        self,
        db: Session,
        user_id: int
    ) -> Sequence[Row | RowMapping | Any]:
        """Получает платежи пользователя (для /users/me/payments)"""
        result = db.execute(select(Payment).filter(Payment.user_id == user_id))
        return result.scalars().all()

    def process_payment_sync(
            self,
            db: Session,
            payment: PaymentCreate
    ) -> Payment | None:
        """Синхронная обработка платежа"""
        # Проверка дубликата транзакции
        existing_payment = db.query(Payment).filter(
            Payment.transaction_id == payment.transaction_id
        ).first()

        if existing_payment:
            return None

        # Создание записи о платеже
        new_payment = Payment(
            transaction_id=payment.transaction_id,
            amount=payment.amount,
            user_id=payment.user_id,
            account_id=payment.account_id
        )

        # Обновление баланса счета
        account = db.query(Account).filter(
            Account.id == payment.account_id,
            Account.user_id == payment.user_id
        ).first()

        if not account:
            account = Account(id=payment.account_id, user_id=payment.user_id)
            db.add(account)

        account.balance += payment.amount
        db.add(new_payment)
        db.commit()

        return new_payment


payment_crud = PaymentCRUD()
