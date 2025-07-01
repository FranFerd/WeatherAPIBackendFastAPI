from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from configs.app_settings import settings

engine = create_engine(url=settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    import models.user
    Base.metadata.create_all(bind=engine)