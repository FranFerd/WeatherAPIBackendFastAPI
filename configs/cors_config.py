from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from configs.app_settings import settings

def add_cors_middleware(app: FastAPI):        
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"], # Allows all HTTP methods (GET, POST, etc.)
        allow_headers=["*"]  # Allows all headers (Authorization, etc.)
    )