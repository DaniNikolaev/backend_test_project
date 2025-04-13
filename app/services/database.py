from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from contextlib import contextmanager
from .config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE
)

Base = declarative_base()

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

def get_db() -> Session:  # Убрали @contextmanager
    db = SessionLocal()
    try:
        return db  # Возвращаем саму сессию, а не генератор
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()