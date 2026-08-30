"""Persistence tests for the auth user repository."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.modules.auth.models import User, UserRole
from vzticket.modules.auth.repository import UserRepository
from vzticket.modules.auth.security import hash_password


async def test_create_user_persists(session: AsyncSession):
    user = User(
        name='John Doe',
        email='john@example.com',
        password_hash=hash_password('supersecret'),
        role=UserRole.CLIENT,
    )

    created = await UserRepository(session).create(user)

    assert created.id is not None
    assert created.email == 'john@example.com'
    assert created.role == UserRole.CLIENT


async def test_get_by_email_returns_user(session: AsyncSession):
    user = User(
        name='John Doe',
        email='john@example.com',
        password_hash=hash_password('supersecret'),
        role=UserRole.CLIENT,
    )
    await UserRepository(session).create(user)

    found = await UserRepository(session).get_by_email('john@example.com')

    assert found is not None
    assert found.id == user.id
    assert found.name == 'John Doe'


async def test_get_by_email_returns_none_when_missing(session: AsyncSession):
    found = await UserRepository(session).get_by_email('ghost@example.com')

    assert found is None


async def test_get_by_id_returns_user(session: AsyncSession):
    user = User(
        name='John Doe',
        email='john@example.com',
        password_hash=hash_password('supersecret'),
        role=UserRole.CLIENT,
    )
    created = await UserRepository(session).create(user)

    found = await UserRepository(session).get_by_id(created.id)

    assert found is not None
    assert found.email == 'john@example.com'


async def test_get_by_id_returns_none_when_missing(session: AsyncSession):
    found = await UserRepository(session).get_by_id(uuid.uuid4())

    assert found is None