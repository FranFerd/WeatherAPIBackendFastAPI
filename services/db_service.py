from sqlalchemy.orm import Session
from models.user import User

class DbService:
    def __init__(self, db: Session):
        self.db = db

    def check_username(self, username: str) -> bool:
        return self.db.query(User).filter(User.username == username).first() is not None

    async def add_user(self, username: str, hashed_password: str):
        new_user = User(username=username, password_hash=hashed_password)

        self.db.add(new_user) # Stage new_user to be added to DB
        self.db.commit()      # Commit transaction - write changes to DB
        self.db.refresh(new_user) # Reloads the instance from DB, ensuring attributs like 'id' are up-to-date

        return new_user