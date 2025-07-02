from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from services.db_service import DbService
from services.auth_service import AuthService

from security.password_hashing import hash_password

from schemas.token import Token
from schemas.user import UserCredentials, UserDb


class UserService:
    def __init__(self, db: Session):
        self.db_service = DbService(db)
        self.auth_service = AuthService(db)
    async def sign_up(self, user_credentials: UserCredentials) -> UserDb:
        if await self.db_service.check_username(user_credentials.username):
            print(f"user_credentials.username: {user_credentials.username}")
            raise HTTPException(status_code=400, detail="Username already exists")
        
        if not user_credentials.username or not user_credentials.password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing credentials')
        
        hashed_password = hash_password(user_credentials.password)
        return await self.db_service.add_user(user_credentials.username, hashed_password)
    
    async def login(self, form_data: OAuth2PasswordRequestForm) -> Token:
        """
            Authenticate user and generate a JWT token.

            - **username**: user's login name
            - **password**: user's password

            Returns an access token to be used for authenticated requests.
        """
        if not form_data.username or not form_data.password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing credentials')

        if not self.auth_service.authenticate_user(form_data.username, form_data.password): # form_data.username = "franz", form_data.password = "secret"
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        
        access_token = self.auth_service.create_access_token(
            data = {"sub": form_data.username},
            expires_delta=timedelta(minutes=15)
        )
        return {"access_token": access_token, "token_type": "bearer"} # token_type: bearer means the client should send the token like Authorization: Bearer <token>
                                                                # "bearer" means "anyone who has this token is authorized - no password required"
