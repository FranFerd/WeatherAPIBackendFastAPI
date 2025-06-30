from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from services.auth_service import decode_token
from services.weather_service import weather_service

from schemas.token import Token, WelcomeMessage, TokenData

router = APIRouter()

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token: # Parses a form with username, password. Request example: username=franz&password=secret
    return await weather_service.login(form_data)

@router.get("/protected", response_model=WelcomeMessage)
async def protected_route(current_user: TokenData = Depends(decode_token)) -> WelcomeMessage:
    return {"message": f"Welcome, {current_user.username}"}

@router.get("/weather/hourly/check-address/{location}")
async def check_address(location: str):
    return await weather_service.check_address(location)

@router.get("/weather/hourly/{location}/{number_of_days}")
async def get_weather_hourly(location: str, number_of_days: int):
    return await weather_service.get_weather_hourly(location, number_of_days)

@router.get("/test/{location}")
async def test(location):
    return weather_service.test(location)