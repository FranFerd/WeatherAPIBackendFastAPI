from dotenv import load_dotenv

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from services.auth_service import decode_token
from services.weather_service import weather_service

from schemas.token import Token, TokenData, WelcomeMessage

app = FastAPI(
    title="Weather API",
    description="This app fetches data from VisualCrossing and caches it using Redis. Has login, sign up",
    version="1.0.0",
    contact={
        "name": "Franz",
        "email": "vlad.solovey7@gmail.com",
    }
)

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
    return weather_service.login(form_data)

@app.get("/protected", response_model=WelcomeMessage)
def protected_route(current_user: TokenData = Depends(decode_token)) -> WelcomeMessage:
    return {"message": f"Welcome, {current_user.username}"}

@app.get("/weather/hourly/check-address/{location}")
def check_address(location: str):
    return weather_service.check_address(location)

@app.get("/weather/hourly/{location}/{number_of_days}")
def get_weather_hourly(location: str, number_of_days: int):
    return weather_service.get_weather_hourly(location, number_of_days)

@app.get("/test/{location}")
def test(location):
    return weather_service.test(location)