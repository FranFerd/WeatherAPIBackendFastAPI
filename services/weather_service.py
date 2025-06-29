import os
from dotenv import load_dotenv
from fastapi import status, HTTPException
from datetime import timedelta
from .auth_service import authenticate_user, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from ..models.token import Token

class WeatherService:
    def login(form_data: OAuth2PasswordRequestForm) -> Token:
        if not form_data.username or not form_data.password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing credentials')
    
        if not authenticate_user(form_data.username, form_data.password): # form_data.username = "franz", form_data.password = "secret"
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        
        access_token = create_access_token(
            data = {"sub": form_data.username},
            expires_delta=timedelta(minutes=15)
        )
        return {"access_token": access_token, "token_type": "bearer"} # token_type: bearer means the client should send the token like Authorization: Bearer <token>
                                                                  # "bearer" means "anyone who has this token is authorized - no password required"