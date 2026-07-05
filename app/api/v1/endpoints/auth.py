from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import Token, UserCreate, OTPVerify, UserLogin
from app.services.user_service import register_new_user, verify_user_otp, login_user



router = APIRouter()

@router.post("/register")
def register_user(user:UserCreate, db:Session=Depends(get_db)):
    return register_new_user(user, db)



@router.post("/verify-otp")
def verify_otp(verify_data:OTPVerify, db:Session = Depends(get_db)):
    return verify_user_otp(verify_data, db)



@router.post("/login", response_model=Token)
def login(login_data:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    return login_user(login_data, db)


@router.get("/profile")
def get_user_profile(current_user: User = Depends(get_current_user)):
    return{
        "message": "Welcome to your profile",
        "email": current_user.email,
        "role": [role.name for role in current_user.roles]
    }