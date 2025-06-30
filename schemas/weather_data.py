from pydantic import BaseModel
from typing import Optional, List

class HourWeather(BaseModel):
    datetime: str
    temp: Optional[float]
    feelslike: Optional[float]
    preciptype: Optional[List[str]] = None
    windspeed: Optional[float]
    uvindex: Optional[float]
    conditions: Optional[str]
    icon: Optional[str]

class DayWeather(HourWeather):
    sunrise: Optional[str]
    sunset: Optional[str]
    hours: Optional[List[HourWeather]] = None

class WeatherDataRefined(BaseModel):
    address: str 
    resolvedAddress: str
    days: List[DayWeather]

class WeatherHourlyResponse(BaseModel):
    weather_data: WeatherDataRefined
    is_cached: bool

class VisualCrossingWeatherData(BaseModel):
    queryCost: int
    latitude: float
    longitude: float
    resolvedAddress: str
    address: str
    timezone: str
    tzoffset: float
    days: List[DayWeather]