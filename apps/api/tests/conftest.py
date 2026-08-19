import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from verzel.core.database import table_registry

engine = create_async_engine(
    'sqlite:aiosqlite:///:memory:',
    connect_args={'check_same_thread': False},
    poolclass=StaticPool
)

TestSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture
async def session():
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)
