from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from configs.app_settings import settings

engine = create_engine(url=settings.DATABASE_URL) # Engine manages database connections and communication

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # sessionmaker creates a session.

Base = declarative_base() # Base is a parent class for models, holds metadata. Metadata holds the complete definition of db schema(tables, columns, relationships)

def init_db():
    import models.user # Loads models into memory so they register with Base.metadata
    Base.metadata.create_all(bind=engine) # create_all creates a table 'users' (__tablename__ = 'users' in models.user.py). Use conditionally

# Session is a workspace for talking to the database, which is used to run queries. Similar to 'cursor' in Flask(refer to libraryProject)   
# Session's don't use raw SQL unlike cursor. It's a high-end, modern way of working with db 

# Base is the foundation of SQLAlchemy's ORM (Object Relational Mapping) system. ORM is a way to use classes to represent and interact with db tables - no raw SQL
# Base mapps every class that inherits from it to a db table
# Base prepares all model classes, so the engine knows how to create and manage them. 
# Any class that inherits from Base is added to metadata