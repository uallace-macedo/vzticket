from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from verzel.core.security.jwt import create_access_token
from verzel.core.security.password import verify_password
from verzel.core.security.types import TokenPayload
from verzel.modules.auth.exceptions import InvalidCredentialsError
from verzel.modules.users.model import User
from verzel.modules.users.schemas import UserCreate
from verzel.modules.users.service import UserService


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.user_service = UserService(session)

    async def register(self, data: UserCreate) -> User:
        """Register a user based on `user_service.create`"""
        user = await self.user_service.create(data)
        return user

    async def login(self, data: OAuth2PasswordRequestForm) -> tuple[str, User]:
        """
        Login a user based on `fastapi.securityOAuth2PasswordRequestForm`
        and returns a `tuple[access_token, User]`
        """
        user = await self.user_service.get_user_by_email(data.username)

        if not user or not verify_password(data.password, user.password):
            raise InvalidCredentialsError()

        payload = TokenPayload(
            sub=user.id,
            email=user.email,
            role=user.role
        )

        access_token = create_access_token(payload)
        return access_token, user
