from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.weather import weather_router
from configs.app_settings import settings
class WeatherAppMainService:
    def __init__(self):
        self.app = FastAPI(
            title="Weather API",
            description="Fetches weather, caches with Redis, supports JWT login.",
            version="1.0.0"
        )

    def configure_cors(self) -> None:
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )
    
    def configure_routers(self) -> None:
        self.app.include_router(weather_router)

    def configure_events(self) -> None:
        @self.app.on_event("startup")
        def startup():
            print("App is starting...")
        
        @self.app.on_event("shutdown")
        def shutdown():
            print("App is shutting down...")
    
    def run(self) -> FastAPI:
        self.configure_cors()
        self.configure_routers()
        self.configure_events()
        return self.app
