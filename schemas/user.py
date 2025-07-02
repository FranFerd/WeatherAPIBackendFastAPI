from pydantic import BaseModel, field_validator

class UserCredentials(BaseModel):
    username: str
    password: str

    @field_validator('username', 'password') # validates username and password
    def not_empty(cls, value: str): #cls is class. Must be included
        if not value or not value.strip():
            raise ValueError('Must not be empty or blank')
        return value