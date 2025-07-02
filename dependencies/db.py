from database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator # Generator is a type hint for describing generator behaviour
                             
async def get_db() -> AsyncGenerator[AsyncSession, None]: # get_db is generator - a function that returns values with yield
    async with SessionLocal() as session:
        yield session
        
# @router.get("/users")
# def read_users(db: Session = Depends(get_db)):
#    users = db.query(User).all()
#     return users

# Depends(get_db) calls the generator. FastAPI yield the db session to the route. After the route returns, FastAPI automatically closes
# the session using finally block

# FastAPI can manage the lifecycle of the dependency if it's a generator function. FastAPI pauses at yield, and resumes to run cleanup

# yield gives FastAPI a "checkpoint" in your function so it can come back after the route finishes and clean up.
