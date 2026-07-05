from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, OTPVerify
from app.services.user_service import register_new_user, verify_user_otp



router = APIRouter()

@router.post("/register")
def register_user(user:UserCreate, db:Session=Depends(get_db)):
    return register_new_user(user, db)



@router.post("/verify-otp")
def verify_otp(verify_data:OTPVerify, db:Session = Depends(get_db)):
    return verify_user_otp(verify_data, db)




    
