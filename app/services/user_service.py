from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.models.user import Role, User
from app.schemas.user import OTPVerify, UserCreate
from app.utils.helpers import generate_otp, send_otp_email
from app.core.constants import RoleNames


class SuccesMessage:
    REGISTRATION_SUCCESS = "User registered successfully! Please check your email for OTP."
    VERIFICATION_SUCCESS = "Account verified successfully! You can now log in."

class ErrorMessage:
    EMAIL_EXISTS = "email already registered."
    USER_NOT_FOUND = "user not found."
    ALREADY_VERIFIED = "Account is already verified."
    INVALID_OTP = "Invalid OTP."



def register_new_user(user:UserCreate, db:Session):

    # check if user exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail=ErrorMessage.EMAIL_EXISTS)
    
    # create default role
    default_role = db.query(Role).filter(Role.name == RoleNames.USER).first()
    if not default_role:
        default_role = Role(name=RoleNames.USER)
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
        "message": SuccesMessage.REGISTRATION_SUCCESS
    }


def verify_user_otp(verify_data:OTPVerify, db:Session):
    user = db.query(User).filter(User.email == verify_data.email).first()

    if not user:
        raise HTTPException(status_code=404, detail=ErrorMessage.USER_NOT_FOUND)
    if user.is_verified:
        raise HTTPException(status_code=400, detail=ErrorMessage.ALREADY_VERIFIED)
    if user.otp != verify_data.otp:
        raise HTTPException(status_code=400, detail=ErrorMessage.INVALID_OTP)
    
    user.is_verified = True
    user.otp = None
    db.commit()

    return{
        "status": "Succes",
        "message": SuccesMessage.VERIFICATION_SUCCESS
    }