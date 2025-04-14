# Базовый образ
FROM python:3.10-slim

# Устанавливаем netcat и зависимости для PostgreSQL
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        libpq-dev \
        netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*  # Правильный отступ и расположение


WORKDIR /app

# Сначала копируем зависимости для кэширования слоев
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Переменные окружения по умолчанию
ENV PYTHONPATH=/app \
    DATABASE_URL=postgresql://postgres:123@db:5432/backend_test_project \
    RESET_DB_ON_STARTUP=false \
    DB_ECHO=false

# Упрощаем команду запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]