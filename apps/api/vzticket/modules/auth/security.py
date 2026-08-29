"""Security utilities for the auth module.

Provides password hashing/verification using pwdlib (Argon2) and JWT
creation/decoding using PyJWT.
"""

from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from pwdlib import PasswordHash

from vzticket.core.config import settings
from vzticket.modules.auth.exceptions import InvalidTokenError

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a plain-text password using Argon2."""
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a stored Argon2 hash."""
    return password_hash.verify(plain_password, hashed_password)


def _create_token(subject: str, expires_delta: timedelta, token_type: str) -> str:
    """Create a signed JWT token for the given subject."""
    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        'sub': subject,
        'type': token_type,
        'iat': now,
        'exp': now + expires_delta,
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def create_access_token(subject: str) -> str:
    """Create a short-lived access token."""
    return _create_token(
        subject,
        timedelta(minutes=settings.access_token_expire_minutes),
        token_type='access',
    )


def create_refresh_token(subject: str) -> str:
    """Create a long-lived refresh token."""
    return _create_token(
        subject,
        timedelta(minutes=settings.refresh_token_expire_minutes),
        token_type='refresh',
    )


def decode_token(token: str, expected_type: str = 'access') -> dict[str, Any]:
    """Decode and validate a JWT token.

    Raises
    ------
    InvalidTokenError
        If the token is malformed, expired, or does not match the expected type.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except jwt.PyJWTError as exc:
        raise InvalidTokenError from exc

    if payload.get('type') != expected_type:
        raise InvalidTokenError

    return payload