import os
from dotenv import load_dotenv

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from schemas.token import TokenData
from schemas.user import User

load_dotenv()

JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRES_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # OAuth2PasswordBearer extracts token from Authorization: Bearer
                                                                # tokeUnrl='token' is the login endpoint that provides the token('/token')
                                                                # oath2_scheme tell fastAPI how to extract token from Authorization header

fake_user: User = {"username": "franz", "password": "secret"}

def authenticate_user(username: str, password: str) -> bool:
    return username == fake_user["username"] and password == fake_user["password"]

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str: #data can be {'sub':'franz'}
    to_encode = data.copy() # to prevent modifying original dict, which could cause bugs if it's reused somewhere
    expires_at = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expires_at})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)

def decode_token(token: str = Depends(oauth2_scheme)) -> TokenData:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=ALGORITHM)
        username: str = payload.get("sub") # subject of the token (username)
        if username is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        return TokenData(username=username)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")