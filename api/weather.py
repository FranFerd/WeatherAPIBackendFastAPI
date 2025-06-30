from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from services.auth_service import decode_token
from services.weather_service import weather_service

from schemas.token import Token, WelcomeMessage, TokenData


weather_router = APIRouter()

@weather_router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token: # Parses a form with username, password. Request example: username=franz&password=secret
    return weather_service.login(form_data)

@weather_router.get("/protected", response_model=WelcomeMessage)
def protected_route(current_user: TokenData = Depends(decode_token)) -> WelcomeMessage:
    return {"message": f"Welcome, {current_user.username}"}

@weather_router.get("/weather/hourly/check-address/{location}")
def check_address(location: str):
    return weather_service.check_address(location)

@weather_router.get("/weather/hourly/{location}/{number_of_days}")
def get_weather_hourly(location: str, number_of_days: int):
    return weather_service.get_weather_hourly(location, number_of_days)

@weather_router.get("/test/{location}")
def test(location):
    return weather_service.test(location)