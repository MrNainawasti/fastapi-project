from datetime import timedelta

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_password_hash, verify_password
from app.models.user import Role, User
from app.schemas.user import OTPVerify, UserCreate, UserLogin, Token
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
    INVALID_CREDENTIALS = "Incorrect email or password!"
    NOT_VERIFIED = "Account not verified! Please verify your account."



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

def login_user(login_data:OAuth2PasswordRequestForm, db:Session) -> Token:

    # check if user exixts
    user = db.query(User).filter(User.email == login_data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail=ErrorMessage.INVALID_CREDENTIALS)
    
    # verify password
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail=ErrorMessage.INVALID_CREDENTIALS)
    
    # check account verification
    if not user.is_verified:
        raise HTTPException(status_code=400, detail=ErrorMessage.NOT_VERIFIED)
    
    # generate JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return Token(access_token = access_token, token_type="bearer")
    


