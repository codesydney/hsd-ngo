import os
from pathlib import Path
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel

# Determine database path
if os.path.exists("/data"):
    # Production on Fly.io - use volume
    DB_PATH = Path("/data/hsd_ngo.db")
else:
    # Development - use local file
    DB_PATH = Path("./hsd_ngo.db")

# Ensure directory exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    async with async_session() as session:
        yield session


async def init_db() -> None:
    """Initialize database and create tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

