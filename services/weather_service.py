from fastapi import status, HTTPException
from datetime import timedelta
from auth_service import authenticate_user, create_access_token
from redis_service import redis_service
from fastapi.security import OAuth2PasswordRequestForm
from models.token import Token
from configs.app_settings import settings
import requests, json
class WeatherService:
    def __init__(self):
        self.api_key = settings.API_KEY
        self.base_url = settings.BASE_URL

    def login(self, form_data: OAuth2PasswordRequestForm) -> Token:
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

    def check_address(self, location: str) -> dict:
        redis_key = f"checkAddress:{location}"
        cached_address = redis_service.get_json(redis_key)
        if cached_address:
            return {"address": cached_address}
        
        url = f'{self.base_url}/{location}'
        params = {
            "unitGroup" : "metric",
            "key" : self.api_key,
            "include" : "address,resolvedAddress",
            "elements": "address,resolvedAddress",
            "content-type" : "json",
            "locationMode" : "single"
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status() # Raises an error, if occured. Without it, there wouldn't be an error, and except isn't executed
        except:
            raise HTTPException(status_code=502, detail="Failed to fetch data from an API") 

        weather_data = response.json()
        address = weather_data.get('address')

        if not address:
            raise ValueError('Invalid address')

        redis_service.set_json(redis_key=redis_key, value=address, time=timedelta(hours=1))
        return {"address": address}          

    # def get_weather_hourly(self, location: str, number_of_days: int):
    #     redis_key = f"weatherHourly:{location}:{number_of_days}"
    #     cached_data = redis_client.get(redis_key)
    #     if cached_data:
    #         return {"weather_data": json.loads(cached_data)}
        
    #     url = f"{self.base_url}/{location}"
    #     params = {
    #         "unitGroup" : "metric",
    #         "key" : self.api_key,
    #         "include" : "hours,resolvedAddress",
    #         "elements": "address,datetime,temp,feelslike,conditions,preciptype,icon,windspeed,uvindex,sunrise,sunset",
    #         "content-type" : "json",
    #         "locationMode" : "single"
    #     }

    #     try:
    #         response = requests.get(url, params=params)
    #         response.raise_for_status() # Raises an error, if occured. Without it, there wouldn't be an error, and except isn't executed
    #     except:
    #         raise HTTPException(status_code=502, detail="Failed to fetch data from an API")
            
    #     weather_data_raw = response.json()
    #     weather_data_refined = {
    #         "address" : weather_data_raw.get("address"),
    #         "resolvedAddress" : weather_data_raw.get("resolvedAddress"),
    #         "days" : weather_data_raw.get("days", [])[:number_of_days]
    #     }

    #     redis_client.setex(
    #         name=redis_key,
    #         time=timedelta(hours=1),
    #         value=json.dumps(weather_data_refined)
    #     )

    #     return {"weather_data": weather_data_refined}                                                        