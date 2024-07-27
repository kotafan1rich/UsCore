from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import MetaData

from src.settings import REAL_DATABSE_URL

engine = create_async_engine(REAL_DATABSE_URL, future=True, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

metadata = MetaData()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
	session = async_session()
	try:
		yield session
	finally:
		await session.close()
