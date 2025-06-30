import requests
from fastapi import HTTPException
from models.url_params import Params

def refine_weather(weather_data_raw, number_of_days: int):
    return {
            "address" : weather_data_raw.get("address"),
            "resolvedAddress" : weather_data_raw.get("resolvedAddress"),
            "days" : weather_data_raw.get("days", [])[:number_of_days]
        }

def fetch_weather(url: str, params: Params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raises an error, if occured. Without it, there wouldn't be an error, and except isn't executed
        return response.json()
    except:
        raise HTTPException(status_code=502, detail="Failed to fetch data from an API")
    