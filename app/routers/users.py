from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserInDB, UserCreate, UserUpdate
from app.crud.user import user_crud
from app.crud.account import account_crud
from app.crud.payment import payment_crud
from app.dependencies import get_current_user, get_current_admin, get_db
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/me/accounts")
async def get_current_user_accounts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return account_crud.get_by_user(db, current_user.id)

@router.get("/me/payments")
async def get_current_user_payments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return payment_crud.get_by_user(db, current_user.id)

@router.put("/me", response_model=UserInDB)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    updated_user = await user_crud.update(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user



@router.get("/", response_model=list[UserInDB], dependencies=[Depends(get_current_admin)])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return user_crud.get_multi(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserInDB, dependencies=[Depends(get_current_admin)])
async def get_specific_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    user = user_crud.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{user_id}/accounts", dependencies=[Depends(get_current_admin)])
async def get_specific_user_accounts(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return account_crud.get_by_user(db, user_id)

@router.get("/{user_id}/payments", dependencies=[Depends(get_current_admin)])
async def get_specific_user_payments(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return payment_crud.get_by_user(db, user_id)

@router.post("/", response_model=UserInDB, status_code=201, dependencies=[Depends(get_current_admin)])
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    existing_user = user_crud.get_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create(db, user)

@router.put("/{user_id}", response_model=UserInDB, dependencies=[Depends(get_current_admin)])
async def update_user(
    user_id: int,
    user: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated_user = user_crud.update(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", dependencies=[Depends(get_current_admin)])
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    success = await user_crud.delete(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}