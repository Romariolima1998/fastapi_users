import asyncio

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient, ASGITransport
from sqlalchemy.pool import StaticPool
import factory

from users.database.models import table_registre
from users.main import app
from users.database.database import get_session
from users.database.models import User
from users.security import hash

class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}password')




@pytest_asyncio.fixture(scope='session')
async def engine():
    engine = create_async_engine(
        "sqlite+aiosqlite:///./test.db",
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(table_registre.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(table_registre.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture()
async def session(engine):
    AsyncSessionLocal = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with AsyncSessionLocal() as session:
        yield session

        async with engine.begin() as conn:
            await conn.run_sync(table_registre.metadata.drop_all)
            await conn.run_sync(table_registre.metadata.create_all)

@pytest_asyncio.fixture()
async def client(session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def user(session):
    pwd = '@Test1234'
    user = UserFactory(password=hash(pwd))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = pwd
    return user


@pytest_asyncio.fixture
async def token(client, user):
    response = await client.post(
        'auth/token',
        data={'username': user.username, 'password': user.clean_password},
    )
    print(f'/n/n {response.json()}/n/n')
    return response.json()['access_token']

