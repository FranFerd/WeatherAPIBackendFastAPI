from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from services.auth_service import AuthService
from services.user_service import UserService

from schemas.token import Token, WelcomeMessage, TokenData
from schemas.user import UserCredentials, UserDb

from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.db import get_db

router = APIRouter()

@router.post("/signup", response_model=UserDb)
async def signup(
    user_credentials: UserCredentials,
    db: AsyncSession = Depends(get_db)) -> UserDb:

    return await UserService(db).sign_up(user_credentials)

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)) -> Token: # Parses a form with username, password. Request example: username=franz&password=secret

    return await UserService(db).login(form_data)

# @router.get("/protected", response_model=WelcomeMessage)
# async def protected_route(current_user: TokenData = Depends(decode_token)) -> WelcomeMessage:
#     return {"message": f"Welcome, {current_user.username}"}