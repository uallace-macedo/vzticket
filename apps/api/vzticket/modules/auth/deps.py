"""Authentication dependencies for the auth module."""

import uuid
from typing import Annotated

from fastapi import Cookie, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.core.config import settings
from vzticket.core.database import get_db
from vzticket.modules.auth.exceptions import InvalidTokenError, UnauthorizedError
from vzticket.modules.auth.models import User
from vzticket.modules.auth.repository import UserRepository
from vzticket.modules.auth.service import AuthService
from vzticket.modules.auth.security import decode_token

# auto_error=False so we can fall back to the HTTP-Only cookie when the
# Authorization header is absent (e.g. browser requests).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login', auto_error=False)


async def get_auth_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AuthService:
    """Provide an AuthService instance with injected UserRepository."""
    return AuthService(repository=UserRepository(db))


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    access_token: Annotated[str | None, Cookie(
        alias=settings.access_token_cookie_name,
    )] = None,
    authorization: Annotated[str | None, Depends(oauth2_scheme)] = None,
) -> User:
    """Resolve the current user from an HTTP-Only cookie or Bearer header.

    The cookie takes precedence; the Bearer header is used as a fallback so the
    Swagger UI "Authorize" button works.
    """
    token = access_token or authorization
    if token is None:
        raise UnauthorizedError

    payload = decode_token(token, expected_type='access')
    subject = payload.get('sub')
    if subject is None:
        raise InvalidTokenError

    try:
        user_id = uuid.UUID(subject)
    except (ValueError, TypeError) as exc:
        raise InvalidTokenError from exc

    user = await UserRepository(db).get_by_id(user_id)
    if user is None:
        raise InvalidTokenError

    return user
