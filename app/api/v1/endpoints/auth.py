from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User, Role
from app.schemas.user import UserCreate, OTPVerify
from app.core.security import get_password_hash
from app.utils.helpers import generate_otp, send_otp_email


router = APIRouter()

@router.post("/register")
def register_user(user:UserCreate, db:Session = Depends(get_db)):

    # check if user exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="email already registered")
    
    # create default role
    default_role = db.query(Role).filter(Role.name == "User").first()
    if not default_role:
        default_role = Role(name ="User")
        db.add(default_role)
        db.commit()
        db.refresh(default_role)

    # generate OTP
    otp = generate_otp()

    # create new user
    new_user = User(
        name = user.name,
        email = user.email,
        password_hash = get_password_hash(user.password),
        phone_number = user.phone_number,
        otp = otp,
        is_verified = False
    )
    new_user.roles.append(default_role)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # send email
    send_otp_email(user.email, otp)

    return{
        "message": "User registered sucessfully! Please check your email for OTP"
    }


@router.post("/verify-otp")
def verify_otp(verify_data:OTPVerify, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.email == verify_data.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_verified:
        raise HTTPException(status_code=400, detail="User is already verified.")
    if user.otp != verify_data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP.")
    
    user.is_verified = True
    user.otp = None
    db.commit()

    return{
        "status": "Success",
        "message": "Account verified sucessfully. You can now log in."
    }




    
