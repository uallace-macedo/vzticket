from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.core.security.jwt import create_access_token, create_refresh_token, decode_refresh_token
from vzticket.core.security.password import verify_password
from vzticket.core.security.types import TokenPayload, TokenType
from vzticket.modules.auth.exceptions import InvalidCredentialsError
from vzticket.modules.users.model import User
from vzticket.modules.users.schemas import UserCreate
from vzticket.modules.users.service import UserService
from vzticket.modules.users.exceptions import UserNotFoundError


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.user_service = UserService(session)

    async def register(self, data: UserCreate) -> User:
        """Register a user based on `user_service.create`"""
        user = await self.user_service.create(data)
        return user

    async def login(self, data: OAuth2PasswordRequestForm) -> tuple[str, str, User]:
        """
        Login a user based on `fastapi.securityOAuth2PasswordRequestForm`
        and returns a `tuple[access_token, User]`
        """
        user = await self.user_service.get_user_by_email(data.username)

        if not user or not verify_password(data.password, user.password):
            raise InvalidCredentialsError()

        payload = TokenPayload(
            sub=user.id,
            type=TokenType.ACCESS,
            email=user.email,
            role=user.role
        )

        access_token = create_access_token(payload)
        refresh_token = create_refresh_token(payload.sub)

        return access_token, refresh_token, user

    async def refresh_access_token(self, refresh_jwt: str) -> str:
        payload = decode_refresh_token(refresh_jwt)

        user_id = payload.get('sub')
        user = await self.user_service.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError('Usuário não encontrado.')

        token_payload = TokenPayload(
            sub=user.id,
            type=TokenType.ACCESS,
            email=user.email,
            role=user.role
        )

        return create_access_token(token_payload)
