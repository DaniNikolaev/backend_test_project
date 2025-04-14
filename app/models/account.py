from sqlalchemy import Column, Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base  # Импортируем из нового файла


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    balance = Column(DECIMAL)

    # Внешний ключ с каскадным удалением
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    # Связь многие-к-одному с User
    owner = relationship("User", back_populates="accounts")

    # Связь один-ко-многим с Payment
    payments = relationship("Payment", back_populates="account", cascade="all, delete-orphan")
