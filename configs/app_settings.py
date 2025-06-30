from pydantic_settings import BaseSettings
from datetime import timedelta
from typing import List

class Settings(BaseSettings):
    API_KEY: str
    JWT_SECRET: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    BASE_URL: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    ALLOWED_ORIGINS: List[str]

    class Config: # Tells Pydantic where to look for env vars
        env_file = ".env"

    @property # Turns a method into an attribute. Now settings.acceess_token_expire instead of settings.access_token_expire()
    def access_token_expire(self) -> timedelta:
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
    

settings = Settings() # settings is a central config object that holds values the app needs to run - usually env vars