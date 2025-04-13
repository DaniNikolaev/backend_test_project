from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Настройки DB (используем синхронный драйвер)
    DATABASE_URL: str = "postgresql://postgres:123@localhost:5432/backend_test_project"  # Изменили на синхронный драйвер
    DB_ECHO: bool = False  # Логирование SQL запросов
    DB_POOL_SIZE: int = 5  # Размер пула подключений
    DB_MAX_OVERFLOW: int = 10  # Максимальное превышение размера пула

    # Настройки аутентификации (если нужны)
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"  # Игнорировать лишние переменные


settings = Settings()