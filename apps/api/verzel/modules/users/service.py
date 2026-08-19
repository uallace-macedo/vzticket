from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from verzel.core.security.password import generate_hash
from verzel.modules.users.exceptions import UserAlreadyExistsError, UserNotFoundError
from verzel.modules.users.model import User
from verzel.modules.users.repository import UserRepository
from verzel.modules.users.schemas import UserCreate


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.user_repository = UserRepository(session)

    async def create(self, data: UserCreate) -> User:
        """Creates a user"""
        user_exists = await self.user_repository.get_by_email(data.email)
        if user_exists:
            raise UserAlreadyExistsError()

        data.password = generate_hash(data.password)
        user = await self.user_repository.create(
            User(**data.model_dump(mode='json'))
        )

        return user

    async def get_user_by_id(self, user_id: UUID) -> User:
        """Get a user by it's id"""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        return user

    async def get_user_by_email(self, email: str) -> User | None:
        """Get a user by it's email"""
        user = await self.user_repository.get_by_email(email)
        return user

    async def get_user_by_email_throws(self, email: str) -> User | None:
        """Get a user by it's email"""
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise UserNotFoundError()

        return user

    async def delete(self, user_id: UUID) -> None:
        """Deletes a user"""
        user = await self.get_user_by_id(user_id)
        await self.user_repository.delete(user)
