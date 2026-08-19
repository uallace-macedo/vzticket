from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from verzel.modules.users.model import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user: User) -> User:
        """Add a new user to db"""
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def get_by_id(self, user_id: UUID) -> User | None:
        """Search a user by it's id"""
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """Search a user by it's email"""
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, user: User) -> None:
        """Deletes a user by it's id"""
        await self.session.delete(user)
        await self.session.commit()
