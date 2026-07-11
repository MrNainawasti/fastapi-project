from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import SECRET_KEY, ALGORITHM
from app.models.user import User


# login route
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token:str = Depends(oauth2_scheme), db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="couldn't validate credentials or token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # token decode
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # extract user ID
        user_id: str = payload.get("sub")
        if user_id == None:
            raise credentials_exception
        
    except JWTError:
        # check for expired or fake token
        raise credentials_exception
    
    # find user in database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user