import os, redis, requests, json
from dotenv import load_dotenv
from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from Backend.WeatherAPIBackendFastAPI.services.auth_service import authenticate_user, create_access_token, decode_token
from services.weather_service import WeatherService

from models.token import Token, TokenData, WelcomeMessage

app = FastAPI()


origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"]  # Allows all headers (Authorization, etc.)
)

load_dotenv()

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token: # Parses a form with username, password. Request example: username=franz&password=secret
    return WeatherService().login(form_data)

@app.get("/protected", response_model=WelcomeMessage)
def protected_route(current_user: TokenData = Depends(decode_token)) -> WelcomeMessage:
    return {"message": f"Welcome, {current_user.username}"}

redis_client = redis.Redis(host="localhost", port=6379, db=0)
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

@app.get("/weather/hourly/check-address/{location}")
def check_address(location: str):
    redis_key = f"checkAddress:{location}"
    cached_data = redis_client.get(redis_key)

    if cached_data:
        return json.loads(cached_data)
    
    url = f'{BASE_URL}/{location}'
    params = {
        "unitGroup" : "metric",
        "key" : API_KEY,
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

    redis_client.setex(
        name=redis_key, 
        time=timedelta(seconds=3600),
        value=json.dumps(address)
    )

    return {"address": address}

@app.get("/weather/hourly/{location}/{number_of_days}")
def get_weather_hourly(location: str, number_of_days: int):
    redis_key = f"weatherHourly:{location}:{number_of_days}"
    cached_data = redis_client.get(redis_key)
    if cached_data:
        return {"weather_data": json.loads(cached_data)}
    
    url = f"{BASE_URL}/{location}"
    params = {
        "unitGroup" : "metric",
        "key" : API_KEY,
        "include" : "hours,resolvedAddress",
        "elements": "address,datetime,temp,feelslike,conditions,preciptype,icon,windspeed,uvindex,sunrise,sunset",
        "content-type" : "json",
        "locationMode" : "single"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raises an error, if occured. Without it, there wouldn't be an error, and except isn't executed
    except:
        raise HTTPException(status_code=502, detail="Failed to fetch data from an API")
        
    weather_data_raw = response.json()
    weather_data_refined = {
        "address" : weather_data_raw.get("address"),
        "resolvedAddress" : weather_data_raw.get("resolvedAddress"),
        "days" : weather_data_raw.get("days", [])[:number_of_days]
    }

    redis_client.setex(
        name=redis_key,
        time=timedelta(hours=1),
        value=json.dumps(weather_data_refined)
    )

    return {"weather_data": weather_data_refined}
