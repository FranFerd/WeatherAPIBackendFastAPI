from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from services.db_service import DbService
from services.auth_service import authenticate_user, create_access_token

from security.password_hashing import hash_password

from schemas.token import Token
from schemas.user import UserCredentials


class UserService:
    def __init__(self, db: Session):
        self.db_service = DbService(db)
    def sign_up(self, form_data: UserCredentials):
        if self.db_service.check_username(form_data.username):
            raise HTTPException(status_code=400, detail="Username already exists")
        
        if not form_data.username or not form_data.password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing credentials')
        
        hashed_password = hash_password(form_data.password)
        return self.db_service.add_user(form_data.username, hashed_password)
    
    async def login(self, form_data: OAuth2PasswordRequestForm) -> Token:
        """
            Authenticate user and generate a JWT token.

            - **username**: user's login name
            - **password**: user's password

            Returns an access token to be used for authenticated requests.
        """
        if not form_data.username or not form_data.password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing credentials')

        if not authenticate_user(form_data.username, form_data.password): # form_data.username = "franz", form_data.password = "secret"
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        
        access_token = create_access_token(
            data = {"sub": form_data.username},
            expires_delta=timedelta(minutes=15)
        )
        return {"access_token": access_token, "token_type": "bearer"} # token_type: bearer means the client should send the token like Authorization: Bearer <token>
                                                                # "bearer" means "anyone who has this token is authorized - no password required"
