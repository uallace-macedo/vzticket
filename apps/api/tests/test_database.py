from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.modules.auth.models import User, UserRole


async def test_database_connection(session: AsyncSession) -> None:
    result = await session.execute(text('SELECT 1'))
    assert result.scalar() == 1


async def test_session_insert_and_query(session: AsyncSession) -> None:
    user = User(
        name='Test User',
        email='test@example.com',
        password_hash='hashed',
        role=UserRole.CLIENT,
    )
    session.add(user)
    await session.commit()

    fetched = await session.get(User, user.id)
    assert fetched is not None
    assert fetched.email == 'test@example.com'
    assert fetched.role == UserRole.CLIENT


async def test_session_rollback(session: AsyncSession) -> None:
    user = User(
        name='Rollback User',
        email='rollback@example.com',
        password_hash='hashed',
    )
    session.add(user)
    await session.flush()
    await session.rollback()

    fetched = await session.get(User, user.id)
    assert fetched is None
