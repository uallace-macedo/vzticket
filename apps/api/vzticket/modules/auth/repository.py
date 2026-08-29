"""Data access layer for the auth module."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.modules.auth.models import User


class UserRepository:
    """Handles raw database operations for :class:`User`."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_email(self, email: str) -> User | None:
        """Return the user with the given email, or ``None`` if not found."""
        result = await self._session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        """Return the user with the given id, or ``None`` if not found."""
        return await self._session.get(User, user_id)

    async def create(self, user: User) -> User:
        """Persist a new user and return it."""
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user
