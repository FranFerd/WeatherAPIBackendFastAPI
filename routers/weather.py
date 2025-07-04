from fastapi import APIRouter, Depends
from services.weather_service import weather_service
from dependencies.decode_token import decode_token
from schemas.token import TokenData

router = APIRouter()

@router.get("/weather/hourly/check-address/{location}")
async def check_address(
    location: str,
    current_user: TokenData = Depends(decode_token)
    ):
    return await weather_service.check_address(location)

@router.get("/weather/hourly/{location}/{number_of_days}")
async def get_weather_hourly(
    location: str,
    number_of_days: int,
    current_user: TokenData = Depends(decode_token)
    ):
    return await weather_service.get_weather_hourly(location, number_of_days)
