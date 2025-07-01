from fastapi import FastAPI
from api.weather import router
from configs.cors_config import add_cors_middleware
from contextlib import asynccontextmanager
from Backend.WeatherAPIBackendFastAPI.database import init_db

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
        self.app.include_router(router)

    def configure_db(self) -> None:
        init_db()

    def register_lifespan(self) -> None: # Manages start up (before yield) and shut down (after yield) logic.
        @asynccontextmanager             # Connect redis, db. Load ML models, clean up on shutdown
        async def lifespan(app: FastAPI):
            print("App is running...")
            yield
            print("App is shutting down...")

        self.app.router.lifespan_context = lifespan
    
    def run(self) -> FastAPI:
        self.configure_cors()
        self.configure_routers()
        self.configure_db()
        return self.app
