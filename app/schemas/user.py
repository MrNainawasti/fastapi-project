from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str
    phone_number:str


class OTPVerify(BaseModel):
    email:EmailStr
    otp:str
    