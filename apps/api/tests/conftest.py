import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from vzticket.core.database import get_session, table_registry
from vzticket.core.security.jwt import create_access_token
from vzticket.core.security.password import generate_hash
from vzticket.core.security.types import TokenPayload
from vzticket.core.settings import settings
from vzticket.main import app
from vzticket.modules.users.model import User, UserRole

engine = create_async_engine(
    'sqlite+aiosqlite:///:memory:',
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


@pytest.fixture
async def client(session):
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
def token(user: User) -> str:
    payload = TokenPayload(
        sub=user.id,
        email=user.email,
        role=user.role,
    )
    return create_access_token(payload)


@pytest.fixture
async def user(session):
    user_obj = User(
        name='test-user',
        email='test@example.com',
        password=generate_hash('password123'),
        role=UserRole.CLIENT
    )
    session.add(user_obj)
    await session.commit()
    await session.refresh(user_obj)
    return user_obj


@pytest.fixture
def auth_client(client: AsyncClient, token: str) -> AsyncClient:
    client.cookies.set(settings.AUTH_COOKIE_NAME, token)
    return client


@pytest.fixture
async def organizer_user(session):
    user_obj = User(
        name='Organizer User',
        email='organizer@example.com',
        password=generate_hash('password123'),
        role=UserRole.ORGANIZER
    )
    session.add(user_obj)
    await session.commit()
    await session.refresh(user_obj)
    return user_obj


@pytest.fixture
def organizer_client(client: AsyncClient, organizer_user: User) -> AsyncClient:
    payload = TokenPayload(
        sub=organizer_user.id,
        email=organizer_user.email,
        role=organizer_user.role,
    )
    token = create_access_token(payload)
    client.cookies.set(settings.AUTH_COOKIE_NAME, token)
    return client
