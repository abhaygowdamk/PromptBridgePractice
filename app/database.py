from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker 
from app.models import Base
import os 
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not configured in .env")

# Convert the Neon URL to SQLAlchemy's asyncpg format
DATABASE_URL = DATABASE_URL.replace(
    "postgresql://",
    "postgresql+asyncpg://",
    1
).split("?")[0]


engine = create_async_engine(DATABASE_URL, echo=True, connect_args={"ssl": "require"})

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

async def get_db():
    async with SessionLocal() as session:
        yield session
