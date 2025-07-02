from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from services.weather_service import weather_service
from services.auth_service import decode_token

from schemas.token import Token, WelcomeMessage, TokenData

router = APIRouter()

@router.post("/signup")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await weather_service.sign_up(form_data)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token: # Parses a form with username, password. Request example: username=franz&password=secret
    return await weather_service.login(form_data)

@router.get("/protected", response_model=WelcomeMessage)
async def protected_route(current_user: TokenData = Depends(decode_token)) -> WelcomeMessage:
    return {"message": f"Welcome, {current_user.username}"}