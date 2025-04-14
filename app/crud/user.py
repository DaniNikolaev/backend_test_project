from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.security import get_password_hash, verify_password


class UserCRUD:
    def __init__(self, model: type[User] = User):
        self.model = model

    def get(self, db: Session, user_id: int) -> User | None:
        """Получить пользователя по ID"""
        return db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        """Получить список пользователей с пагинацией"""
        return db.query(User).offset(skip).limit(limit).all()

    def create(self, db: Session, user_in: UserCreate) -> User:
        """Создать нового пользователя"""
        hashed_password = get_password_hash(user_in.password)
        user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            full_name=user_in.full_name,
            is_admin=getattr(user_in, 'is_admin', False)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, db: Session, user_id: int, user_in: UserUpdate) -> User | None:
        """Обновить данные пользователя"""
        user = self.get(db, user_id)
        if not user:
            return None

        update_data = user_in.dict(exclude_unset=True)
        if 'password' in update_data:
            update_data['hashed_password'] = get_password_hash(update_data.pop('password'))

        for field, value in update_data.items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user

    def delete(self, db: Session, user_id: int) -> bool:
        """Удалить пользователя"""
        user = self.get(db, user_id)
        if not user:
            return False

        db.delete(user)
        db.commit()
        return True

    def authenticate(self, db: Session, email: str, password: str) -> User | None:
        """Аутентификация пользователя"""
        user = self.get_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user


# Экземпляр для использования в зависимостях
user_crud = UserCRUD()
