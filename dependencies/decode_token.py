from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from configs.app_settings import settings

from schemas.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def decode_token(token: str = Depends(oauth2_scheme)) -> TokenData:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=settings.ALGORITHM)
        username: str = payload.get("sub") # subject of the token (username)
        if username is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        return TokenData(username=username)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")