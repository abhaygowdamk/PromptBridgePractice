from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker 
from app.models import Base



DATABASE_URL = "sqlite+aiosqlite:///./app.db"

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

async def get_db():
    async with SessionLocal() as session:
        yield session
