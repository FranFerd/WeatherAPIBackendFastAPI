from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from configs.app_settings import settings

engine = create_async_engine(url=settings.DATABASE_URL, echo=True) # Engine manages database connections and communication

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession) # sessionmaker creates a session.

Base = declarative_base() # Base is a parent class for models, holds metadata. Metadata holds the complete definition of db schema(tables, columns, relationships)

async def create_tables():
    async with engine.begin() as conn: # async with automatically handles setup and cleanup, no 'finally: clean_up()'  
        await conn.run_sync(Base.metadata.create_all) # Base.metadata.create_all is a synchronous function that creates all tables in the database based on your models.
# conn.run_sync() is a helper method provided by SQLAlchemy async connection to run synchronous code safely within an async context.

# AsyncSession is a workspace for talking to the database, which is used to run queries. Similar to 'cursor' in Flask(refer to libraryProject)   
# AsyncSession's don't use raw SQL unlike cursor. It's a high-end, modern way of working with db 

# Base is the foundation of SQLAlchemy's ORM (Object Relational Mapping) system. ORM is a way to use classes to represent and interact with db tables - no raw SQL
# Base mapps every class that inherits from it to a db table
# Base prepares all model classes, so the engine knows how to create and manage them. 
# Any class that inherits from Base is added to metadata