from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.common.db import get_db
from src.schemas.user import User, UserCreate
from src.crud.user import create_user, get_user_by_id

router = APIRouter()

@router.post("/", response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db=db, user=user)
    return db_user

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
