from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user import User

from security.password_hashing import verify_password

class DbService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_username(self, username: str) -> bool:
        result = await self.db.execute(
            select(User).filter(User.username == username)
        )
        user = result.scalars().first()
        return user

    async def add_user(self, username: str, hashed_password: str):
        new_user = User(username=username, password_hash=hashed_password)

        self.db.add(new_user) # Stage new_user to be added to DB. add is sync, no await
        await self.db.commit()      # Commit transaction - write changes to DB
        await self.db.refresh(new_user) # Reloads the instance from DB, ensuring attributs like 'id' are up-to-date

        return new_user
    
    async def authenticate_user(self, username: str, password: str) -> bool:
        result = await self.db.execute(
            select(User.password_hash)
            .filter(User.username == username)
        )
        hashed_password = result.scalar_one_or_none()

        if hashed_password is None: 
            return False
        
        is_valid_password = verify_password(password, hashed_password)
        return is_valid_password