from fastapi import status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta

from services.auth_service import authenticate_user, create_access_token
from services.redis_service import redis_service

from schemas.token import Token
from schemas.address import Address
from schemas.weather_data import WeatherHourlyResponse

from configs.app_settings import settings

from utils.weather_data import fetch_data, refine_weather
from utils.api_params import get_params_check_address, get_params_weather
class WeatherService:
    def __init__(self):
        self.api_key = settings.API_KEY
        self.base_url = settings.BASE_URL

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

    async def check_address(self, location: str) -> Address:
        redis_key = f"checkAddress:{location}"
        cached_address = await redis_service.get_cached(redis_key)
        if cached_address.is_cached == True:
            return {"address": cached_address}
        
        url = f'{self.base_url}/{location}'
        params = get_params_check_address(self.api_key)

        weather_data = await fetch_data(url, params)
        address = weather_data.address

        if not address:
            raise ValueError('Invalid address')

        await redis_service.set_json(redis_key=redis_key, value=address, time=timedelta(hours=1))
        return {"address": address}          

    async def get_weather_hourly(self, location: str, number_of_days: int) -> WeatherHourlyResponse:
        redis_key = f"weatherHourly:{location}:{number_of_days}"
        cached_weather_hourly = await redis_service.get_cached(redis_key)
        if cached_weather_hourly.is_cached == True:
            return {"weather_data": cached_weather_hourly.data, "is_cached": True}
        
        url = f"{self.base_url}/{location}"
        params = get_params_weather(self.api_key)

        weather_data_raw = await fetch_data(url, params)
        weather_data_refined = refine_weather(weather_data_raw, number_of_days) 

        await redis_service.set_json(redis_key=redis_key, value=weather_data_refined, time=timedelta(hours=1))
        return {"weather_data": weather_data_refined, "is_cached": False}   

    def test(self, location):
        url = f"{self.base_url}/{location}"
        params = get_params_weather(self.api_key)
        return fetch_data(url, params)                                                     

weather_service = WeatherService()