from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from services.auth_service import decode_token
from services.user_service import UserService

from schemas.token import Token, WelcomeMessage, TokenData
from schemas.user import UserCredentials

from sqlalchemy.orm import Session
from dependencies.db import get_db

router = APIRouter()

@router.post("/signup")
async def login(
    form_data: UserCredentials,
    db: Session = Depends(get_db)):

    return await UserService(db).sign_up(form_data)

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)) -> Token: # Parses a form with username, password. Request example: username=franz&password=secret

    return await UserService(db).login(form_data)

@router.get("/protected", response_model=WelcomeMessage)
async def protected_route(current_user: TokenData = Depends(decode_token)) -> WelcomeMessage:
    return {"message": f"Welcome, {current_user.username}"}