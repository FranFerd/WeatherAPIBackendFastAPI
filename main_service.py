from fastapi import FastAPI
from api.weather import router
from configs.cors_config import add_cors_middleware

class WeatherAppMainService:
    def __init__(self):
        self.app = FastAPI(
            title="Weather API",
            description="Fetches weather, caches with Redis, supports JWT login.",
            version="1.0.0"
        )

    def configure_cors(self) -> None:
        add_cors_middleware(self.app)
    
    def configure_routers(self) -> None:
        self.app.include_router(router)

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
