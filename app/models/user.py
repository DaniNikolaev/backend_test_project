from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base  # Импортируем из нового файла


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Связь один-ко-многим с Account
    accounts = relationship("Account", back_populates="owner", cascade="all, delete-orphan")

    # Связь один-ко-многим с Payment
    payments = relationship("Payment", back_populates="user")
