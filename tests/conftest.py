import os

import pytest
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.database import db_helper
from src.main import app
from src.models import Base
from src.users.auth import create_access_token
from tests.utils import load_prepared_data

async_engine = create_async_engine(
    "postgresql+asyncpg://test:test@localhost:5432/fastapi_test",
    echo=False
)
async_session_factory = async_sessionmaker(bind=async_engine)


async def get_session_override():
    async with async_session_factory() as session:
        yield session


app.dependency_overrides = {
    db_helper.scoped_session_dependency: get_session_override
}


@pytest.fixture(autouse=True, scope="session")
async def prepare_db():
    fixture_path = os.path.join(os.path.dirname(__file__), 'fixture.json')
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session_factory() as session:
        await load_prepared_data(fixture_path, session)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
async def unauthorized_client_fixture():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://127.0.0.1:8000"
    ) as ac:
        yield ac


@pytest.fixture(scope='session')
async def authenticated_client_fixture() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://127.0.0.1:8000",
        cookies={"Authorization": create_access_token({"sub": "101"})}
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
async def superuser_fixture() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://127.0.0.1:8000",
            cookies={"Authorization": create_access_token({"sub": "100"})}
    ) as ac:
        yield ac
