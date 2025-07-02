from fastapi import APIRouter
from services.weather_service import weather_service

router = APIRouter()

@router.get("/weather/hourly/check-address/{location}")
async def check_address(location: str):
    return await weather_service.check_address(location)

@router.get("/weather/hourly/{location}/{number_of_days}")
async def get_weather_hourly(location: str, number_of_days: int):
    return await weather_service.get_weather_hourly(location, number_of_days)
