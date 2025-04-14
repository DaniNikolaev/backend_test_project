from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from app.services.security import get_password_hash
from app.models.base import Base
from .config import settings


engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)


def get_db() -> Session:
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def create_test_data() -> None:
    from app.models.user import User  # pylint: disable=import-outside-toplevel
    from app.models.account import Account  # pylint: disable=import-outside-toplevel
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.email == "admin@admin.com").first():
            test_user = User(
                email="admin@admin.com",
                hashed_password=get_password_hash("testpassword"),
                full_name="Admin User",
                is_active=True,
                is_admin=True
            )
            db.add(test_user)
            db.commit()

            test_account = Account(user_id=test_user.id, balance=1000.00)
            db.add(test_account)
            db.commit()
            print("Test data created successfully")
        else:
            print("Test data already exists")
    except SQLAlchemyError as e:
        print(f"Error creating test data: {e}")
        db.rollback()
    finally:
        db.close()


def init_db():
    """Инициализация таблиц БД"""

    if settings.RESET_DB_ON_STARTUP:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database tables initialized")


def check_db_initialized() -> bool:
    """Проверяет, существует ли хотя бы одна таблица"""
    inspector = inspect(engine)
    tables_exist = bool(inspector.get_table_names())
    print(f"Database initialized check: {tables_exist}")
    return tables_exist
