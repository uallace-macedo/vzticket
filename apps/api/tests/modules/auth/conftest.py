"""Shared fixtures for the auth module tests."""

import uuid

import pytest

from vzticket.core.config import settings
from vzticket.modules.auth.models import User, UserRole
from vzticket.modules.auth.repository import UserRepository
from vzticket.modules.auth.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
)


class FakeUserRepository:
    """In-memory repository used for service unit tests."""

    def __init__(self) -> None:
        self._users: dict[uuid.UUID, User] = {}

    async def get_by_email(self, email: str) -> User | None:
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return self._users.get(user_id)

    async def create(self, user: User) -> User:
        user.id = uuid.uuid4()
        self._users[user.id] = user
        return user


@pytest.fixture
def user_payload() -> dict[str, str]:
    """Standard registration payload for a CLIENT user."""
    return {
        'name': 'John Doe',
        'email': 'john@example.com',
        'password': 'supersecret',
        'role': 'CLIENT',
    }


@pytest.fixture
async def registered_user(session) -> User:
    """Insert a standard user in the database and return the instance."""
    user = User(
        name='John Doe',
        email='john@example.com',
        password_hash=hash_password('supersecret'),
        role=UserRole.CLIENT,
    )
    return await UserRepository(session).create(user)


@pytest.fixture
async def authenticated_client(client, registered_user):
    """AsyncClient pre-populated with valid auth cookies for the user."""
    client.cookies.set(
        settings.access_token_cookie_name,
        create_access_token(str(registered_user.id)),
    )
    client.cookies.set(
        settings.refresh_token_cookie_name,
        create_refresh_token(str(registered_user.id)),
    )
    return client


@pytest.fixture
def fake_repository() -> FakeUserRepository:
    """Fresh in-memory repository for service unit tests."""
    return FakeUserRepository()