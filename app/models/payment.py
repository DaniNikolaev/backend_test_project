from sqlalchemy import Column, Integer, DECIMAL, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(DECIMAL)
    transaction_id = Column(String, unique=True, index=True)  # Добавлено по ТЗ

    # Внешний ключ к Account
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"))

    # Внешний ключ к User
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    # Связь многие-к-одному с Account
    account = relationship("Account", back_populates="payments")

    # Связь многие-к-одному с User
    user = relationship("User", back_populates="payments")

