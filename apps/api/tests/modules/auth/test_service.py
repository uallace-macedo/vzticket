"""Unit tests for the auth service and security utilities."""

import uuid
from datetime import UTC, datetime, timedelta

import jwt
import pytest

from vzticket.core.config import settings
from vzticket.modules.auth.exceptions import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    InvalidTokenError,
)
from vzticket.modules.auth.models import User, UserRole
from vzticket.modules.auth.schemas import UserRegister
from vzticket.modules.auth.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from vzticket.modules.auth.service import AuthService


# --- Password hashing ---


def test_hash_password_creates_verifiable_hash():
    hashed = hash_password('supersecret')

    assert hashed != 'supersecret'
    assert verify_password('supersecret', hashed)


def test_verify_password_rejects_wrong_password():
    hashed = hash_password('supersecret')

    assert not verify_password('wrong-password', hashed)


# --- register_user ---


async def test_register_user_creates_user(fake_repository):
    service = AuthService(repository=fake_repository)
    data = UserRegister(
        name='John Doe',
        email='john@example.com',
        password='supersecret',
        role=UserRole.CLIENT,
    )

    user = await service.register_user(data)

    assert user.id is not None
    assert user.email == 'john@example.com'
    assert user.password_hash != 'supersecret'
    assert verify_password('supersecret', user.password_hash)


async def test_register_user_duplicate_email_raises(fake_repository):
    service = AuthService(repository=fake_repository)
    data = UserRegister(
        name='John Doe',
        email='john@example.com',
        password='supersecret',
        role=UserRole.CLIENT,
    )
    await service.register_user(data)

    with pytest.raises(EmailAlreadyRegisteredError):
        await service.register_user(data)


# --- authenticate_user ---


async def test_authenticate_user_success(fake_repository):
    service = AuthService(repository=fake_repository)
    data = UserRegister(
        name='John Doe',
        email='john@example.com',
        password='supersecret',
        role=UserRole.CLIENT,
    )
    await service.register_user(data)

    user = await service.authenticate_user('john@example.com', 'supersecret')

    assert user.email == 'john@example.com'


async def test_authenticate_user_wrong_password_raises(fake_repository):
    service = AuthService(repository=fake_repository)
    data = UserRegister(
        name='John Doe',
        email='john@example.com',
        password='supersecret',
        role=UserRole.CLIENT,
    )
    await service.register_user(data)

    with pytest.raises(InvalidCredentialsError):
        await service.authenticate_user('john@example.com', 'wrong-password')


async def test_authenticate_user_unknown_email_raises(fake_repository):
    service = AuthService(repository=fake_repository)

    with pytest.raises(InvalidCredentialsError):
        await service.authenticate_user('ghost@example.com', 'supersecret')


# --- refresh_tokens ---


async def test_refresh_tokens_issues_new_pair(fake_repository):
    service = AuthService(repository=fake_repository)
    data = UserRegister(
        name='John Doe',
        email='john@example.com',
        password='supersecret',
        role=UserRole.CLIENT,
    )
    user = await service.register_user(data)
    refresh_token = create_refresh_token(str(user.id))

    tokens = await service.refresh_tokens(refresh_token)

    assert 'access_token' in tokens
    assert 'refresh_token' in tokens
    assert decode_token(tokens['access_token'], expected_type='access')['sub'] == str(
        user.id
    )


async def test_refresh_tokens_with_access_token_raises(fake_repository):
    service = AuthService(repository=fake_repository)
    data = UserRegister(
        name='John Doe',
        email='john@example.com',
        password='supersecret',
        role=UserRole.CLIENT,
    )
    user = await service.register_user(data)
    access_token = create_access_token(str(user.id))

    with pytest.raises(InvalidTokenError):
        await service.refresh_tokens(access_token)


async def test_refresh_tokens_unknown_user_raises(fake_repository):
    service = AuthService(repository=fake_repository)
    refresh_token = create_refresh_token(str(uuid.uuid4()))

    with pytest.raises(InvalidTokenError):
        await service.refresh_tokens(refresh_token)


# --- token decoding / expiration ---


def test_decode_token_returns_payload():
    token = create_access_token('user-123')

    payload = decode_token(token, expected_type='access')

    assert payload['sub'] == 'user-123'
    assert payload['type'] == 'access'


def test_decode_token_wrong_type_raises():
    token = create_access_token('user-123')

    with pytest.raises(InvalidTokenError):
        decode_token(token, expected_type='refresh')


def test_decode_token_malformed_raises():
    with pytest.raises(InvalidTokenError):
        decode_token('not-a-valid-token', expected_type='access')


def test_decode_token_expired_raises():
    now = datetime.now(UTC)
    payload = {
        'sub': 'user-123',
        'type': 'access',
        'iat': now - timedelta(hours=2),
        'exp': now - timedelta(hours=1),
    }
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

    with pytest.raises(InvalidTokenError):
        decode_token(token, expected_type='access')


def test_decode_token_wrong_signature_raises():
    now = datetime.now(UTC)
    payload = {
        'sub': 'user-123',
        'type': 'access',
        'iat': now,
        'exp': now + timedelta(minutes=15),
    }
    token = jwt.encode(payload, 'a-different-secret', algorithm=settings.algorithm)

    with pytest.raises(InvalidTokenError):
        decode_token(token, expected_type='access')