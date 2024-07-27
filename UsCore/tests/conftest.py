import asyncio
from typing import AsyncGenerator
import pytest
import pytest_asyncio

from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from httpx import AsyncClient, ASGITransport

from src.config import POSTGRES_TEST_HOST, POSTGRES_TEST_NAME, POSTGRES_TEST_PASSWORD, POSTGRES_TEST_PORT, \
    POSTGRES_TEST_USER
from src.db.session import async_session, get_db, metadata
from src.main import app

DATA_BASE_URL_TEST = f"postgresql+asyncpg://{POSTGRES_TEST_USER}:{POSTGRES_TEST_PASSWORD}@{POSTGRES_TEST_HOST}:{POSTGRES_TEST_PORT}/{POSTGRES_TEST_NAME}"

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

engine_test = create_async_engine(DATA_BASE_URL_TEST, poolclass=NullPool)
async_session_test = async_sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)

metadata.bind = engine_test


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    session = async_session()
    try:
        yield session
    finally:
        await session.close()


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(scope='session', autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop_policy():
    policy = asyncio.get_event_loop_policy()
    asyncio.set_event_loop_policy(policy)
    return policy


@pytest.fixture(scope="session")
def event_loop(event_loop_policy):
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def client():
    a = AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost")
    yield a
