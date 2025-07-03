from configs.app_settings import settings

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from schemas.token import TokenData

from services.db_service import DbService
from services.redis_service import redis_service

from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # OAuth2PasswordBearer extracts token from Authorization: Bearer
# tokenUnrl='token' is the login endpoint that provides the token('/token')
# oath2_scheme tell fastAPI how to extract token from Authorization header

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.db_service = DbService(db)
    async def is_correct_credentials(self, username: str, password: str) -> bool:
        return await self.db_service.authenticate_user(username, password)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str: # data can be {'sub':'franz'}
        to_encode = data.copy() # to prevent modifying original dict, which could cause bugs if it's reused somewhere
        expires_at = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expires_at})
        return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

    def decode_token(self, token: str = Depends(oauth2_scheme)) -> TokenData:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=settings.ALGORITHM)
            username: str = payload.get("sub") # subject of the token (username)
            if username is None:
                raise HTTPException(status_code=400, detail="Invalid token")
            return TokenData(username=username)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
        
    async def authenticate_user(self, username: str, password: str) -> bool:
        await redis_service.is_blocked(username)

        is_authenticated = await self.is_correct_credentials(username, password)

        if not is_authenticated:
            await redis_service.register_failed_attempt(username)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        
        await redis_service.reset_attempts(username)
        return True