from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.crud import base, user
from app.database import get_session
from app.schemas import CreateUser, UpdateUser, UserResponse


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/", response_model=list[UserResponse])
async def list_users(skip: int = 0, limit: int = 10, show_deleted: bool = False, db: Session = Depends(get_session)):
    return await base.all(db, user.User, skip=skip, limit=limit, show_deleted=show_deleted)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_session)):
    user_obj = await base.get(db, user.User, id=user_id)

    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return user_obj

@router.post("/", response_model=UserResponse)
async def create_user(user_data: CreateUser, db: Session = Depends(get_session)):
    return await user.create_user(db, payload=user_data)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UpdateUser, db: Session = Depends(get_session)):
    user_obj = await base.get(db, user.User, id=user_id)

    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return await user.update_user(db, user_obj=user_obj, user_data=user_data)

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_session)):
    await base.delete(db, user.User, id=user_id)
 
