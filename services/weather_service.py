import requests
from fastapi import status, HTTPException
from datetime import timedelta
from services.auth_service import authenticate_user, create_access_token
from services.redis_service import redis_service
from fastapi.security import OAuth2PasswordRequestForm
from models.token import Token
from configs.app_settings import settings
from models.address import AddressResponse
from utils.get_weather_data import fetch_weather, refine_weather
from utils.get_api_params import get_params_check_address, get_params_weather
class WeatherService:
    def __init__(self):
        self.api_key = settings.API_KEY
        self.base_url = settings.BASE_URL

    def login(self, form_data: OAuth2PasswordRequestForm) -> Token:
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

    def check_address(self, location: str) -> AddressResponse:
        redis_key = f"checkAddress:{location}"
        cached_address = redis_service.get_json(redis_key)
        if cached_address:
            return {"address": cached_address}
        
        url = f'{self.base_url}/{location}'
        params = get_params_check_address(self.api_key)

        weather_data = fetch_weather(url, params)
        address = weather_data.get('address')

        if not address:
            raise ValueError('Invalid address')

        redis_service.set_json(redis_key=redis_key, value=address, time=timedelta(hours=1))
        return {"address": address}          

    def get_weather_hourly(self, location: str, number_of_days: int):
        redis_key = f"weatherHourly:{location}:{number_of_days}"
        cached_weather_hourly = redis_service.get_json(redis_key)
        if cached_weather_hourly:
            return {"weather_data": cached_weather_hourly}
        
        url = f"{self.base_url}/{location}"
        params = get_params_weather(self.api_key)

        weather_data_raw = fetch_weather(url, params)
        weather_data_refined = refine_weather(weather_data_raw, number_of_days) 

        redis_service.set_json(redis_key=redis_key, value=weather_data_refined, time=timedelta(hours=1))
        return {"weather_data": weather_data_refined}                                                        

weather_service = WeatherService()