import httpx
from fastapi import HTTPException
from schemas.url_params import Params
from schemas.weather_data import WeatherDataRefined, VisualCrossingWeatherData

async def fetch_data(url: str, params: Params) -> VisualCrossingWeatherData:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=url, params=params)
            response.raise_for_status() # Raises an error, if occured. Without it, there wouldn't be an error, and except isn't executed
            data = response.json()
            return VisualCrossingWeatherData.model_validate(data)
    except httpx.RequestError as e:
        print(f"Error fetching weather data: {e}")
        raise HTTPException(status_code=502, detail="Failed to fetch data from an API")
    
def refine_weather(weather_data_raw: VisualCrossingWeatherData, number_of_days: int) -> WeatherDataRefined:
    return WeatherDataRefined(
        address=weather_data_raw.address,
        resolvedAddress=weather_data_raw.resolvedAddress,
        days=weather_data_raw.days[:number_of_days]
    )