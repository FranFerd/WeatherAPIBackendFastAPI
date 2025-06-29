from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",
]

def add_cors_middleware(app):        
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"], # Allows all HTTP methods (GET, POST, etc.)
        allow_headers=["*"]  # Allows all headers (Authorization, etc.)
    )