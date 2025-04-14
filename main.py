from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.orm import Session

from app.models import User
from app.routers import auth, users, payments
from app.services.database import check_db_initialized, init_db, create_test_data, get_db

app = FastAPI()
api_router = APIRouter()  # Создаем APIRouter для корневого маршрута

# Подключаем все роутеры
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(payments.router)


@app.on_event('startup')
async def startup_event():
    if not check_db_initialized():
        init_db()
        create_test_data()


@api_router.get("/")
async def read_root(db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == "admin@admin.com").first()
        if user:
            status = "active" if user.is_active else "inactive"
            return {"message": f"Hello, {user.full_name}! (Status: {status})"}
        return {"message": "Admin User not found."}
    except Exception as e:
        return {"message": f"Error: {str(e)}"}

app.include_router(api_router)
