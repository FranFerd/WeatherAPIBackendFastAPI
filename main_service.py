from fastapi import FastAPI
from routers.weather import router as weather_router
from routers.auth import router as auth_router
from configs.cors_config import add_cors_middleware
from contextlib import asynccontextmanager
from database import create_tables

class WeatherAppMainService:
    def __init__(self):
        self.app = FastAPI(
            title="Weather API",
            description="Fetches weather, caches with Redis, supports JWT login.",
            version="1.0.0"
        )
        self.register_lifespan()

    def configure_cors(self) -> None:
        add_cors_middleware(self.app)
    
    def configure_routers(self) -> None:
        self.app.include_router(weather_router)
        self.app.include_router(auth_router)

    def register_lifespan(self) -> None: # Manages start up (before yield) and shut down (after yield) logic.
        @asynccontextmanager             # Connect redis, db. Load ML models, clean up on shutdown
        async def lifespan(app: FastAPI):
            print("App is running...")
            await create_tables()
            yield
            print("App is shutting down...")

        self.app.router.lifespan_context = lifespan
    
    def run(self) -> FastAPI: # Everything here doesn't need cleanup, so it's not in lifespan
        self.configure_cors()
        self.configure_routers()
        return self.app
