from fastapi import FastAPI, APIRouter
from app.routers import auth, users, payments
from app.services.database import engine
from app.models.base import Base
from passlib.context import CryptContext

app = FastAPI()
api_router = APIRouter()  # Создаем APIRouter для корневого маршрута

# Подключаем все роутеры
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(payments.router)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.on_event("startup")
def startup():
    try:
        with engine.connect() as connection:
            # Принудительно пересоздаём таблицы (только для разработки!)
            Base.metadata.drop_all(bind=engine)
            Base.metadata.create_all(bind=engine)
        print("Database reinitialized with new schema.")
    except Exception as e:
        print(f"Database initialization failed: {e}")
        return

    from app.services.database import SessionLocal
    from app.models import User, Account

    db = SessionLocal()
    try:
        if not db.query(User).filter(User.email == "test@example.com").first():
            test_user = User(
                email="test@example.com",
                hashed_password=pwd_context.hash("testpassword"),
                full_name="Test User",
                is_active=True,  # Теперь это поле есть в модели
                is_admin=True
            )
            db.add(test_user)
            db.commit()

            test_account = Account(user_id=test_user.id, balance=1000.00)
            db.add(test_account)
            db.commit()
            print("Test user created successfully with is_active=True.")
        else:
            print("Test user already exists. Consider dropping the database for updates.")
    except Exception as e:
        print(f"Error creating test user: {e}")
    finally:
        db.close()

@api_router.get("/")
async def read_root():
    from app.services.database import SessionLocal
    from app.models import User
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "test@example.com").first()
        if user:
            status = "active" if user.is_active else "inactive"
            return {"message": f"Hello, {user.full_name}! (Status: {status})"}
        else:
            return {"message": "Test User not found. Check logs for creation errors."}
    except Exception as e:
        return {"message": f"Error getting user: {e}"}
    finally:
        db.close()

app.include_router(api_router)