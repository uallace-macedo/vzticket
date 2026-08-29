"""Business logic for the auth module."""

import uuid

from vzticket.modules.auth.exceptions import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    InvalidTokenError,
)
from vzticket.modules.auth.models import User
from vzticket.modules.auth.repository import UserRepository
from vzticket.modules.auth.schemas import UserRegister
from vzticket.modules.auth.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


class AuthService:
    """Encapsulates authentication business rules."""

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def register_user(self, data: UserRegister) -> User:
        """Register a new user.

        Raises
        ------
        EmailAlreadyRegisteredError
            If a user with the same email already exists.
        """
        existing = await self._repository.get_by_email(data.email)
        if existing is not None:
            raise EmailAlreadyRegisteredError

        user = User(
            name=data.name,
            email=data.email,
            password_hash=hash_password(data.password),
            role=data.role,
        )
        return await self._repository.create(user)

    async def authenticate_user(self, email: str, password: str) -> User:
        """Authenticate a user by email and password.

        Raises
        ------
        InvalidCredentialsError
            If the email does not exist or the password does not match.
        """
        user = await self._repository.get_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError
        return user

    async def refresh_tokens(self, refresh_token: str) -> dict[str, str]:
        """Issue a new access token from a valid refresh token.

        Raises
        ------
        InvalidTokenError
            If the refresh token is invalid, expired, or the user no longer exists.
        """
        payload = decode_token(refresh_token, expected_type='refresh')
        subject = payload.get('sub')
        if subject is None:
            raise InvalidTokenError

        try:
            user_id = uuid.UUID(subject)
        except (ValueError, TypeError) as exc:
            raise InvalidTokenError from exc

        user = await self._repository.get_by_id(user_id)
        if user is None:
            raise InvalidTokenError

        return {
            'access_token': create_access_token(str(user.id)),
            'refresh_token': create_refresh_token(str(user.id)),
        }
