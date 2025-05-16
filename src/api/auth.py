from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.services.auth_service import AuthService
from src.db.database import get_db

router = APIRouter()

class UserLogin(BaseModel):
    username: str
    password: str

class UserRegistration(BaseModel):
    username: str
    password: str
    invite_code: str

@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    token = auth_service.authenticate_user(user.username, user.password)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": token}

@router.post("/register")
async def register(user: UserRegistration, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    success = auth_service.register_user(user.username, user.password, user.invite_code)
    if not success:
        raise HTTPException(status_code=400, detail="Registration failed")
    return {"message": "User registered successfully"}