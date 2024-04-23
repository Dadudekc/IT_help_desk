from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import declarative_base, Session
from ..utils.database import get_db
from ..models.models import User
from ..services.security import get_password_hash, verify_password
from pydantic import BaseModel



router = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"username": db_user.username, "id": db_user.id}

@router.post("/login")
def login_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user and verify_password(user.password, db_user.hashed_password):
        return {"message": "Login successful"}
    raise HTTPException(status_code=400, detail="Invalid username or password")

