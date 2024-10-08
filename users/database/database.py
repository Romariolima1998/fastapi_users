from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from users.settings import Settings

engine = create_async_engine(Settings().DATABASE_URL)

async_session = sessionmaker(engine, class_=AsyncSession)

async def get_session():
    async with async_session() as session:
        yield session