from datetime import datetime, timedelta, timezone

import pytest
from jwt import encode

from vzticket.core.security.exceptions import InvalidTokenError, ExpiredTokenError
from vzticket.core.security.jwt import create_access_token, decode_access_token
from vzticket.core.settings import settings


def test_create_and_decode_token_success(valid_payload):
    token = create_access_token(valid_payload)
    decoded = decode_access_token(token)

    assert decoded.sub == valid_payload.sub
    assert decoded.email == valid_payload.email
    assert decoded.role == valid_payload.role


def test_decode_token_expired_raises_error(valid_payload):
    expired_time = datetime.now(tz=timezone.utc) - timedelta(minutes=10)
    raw_payload = valid_payload.model_dump(mode='json')
    raw_payload['exp'] = expired_time

    expired_token = encode(
        payload=raw_payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    with pytest.raises(ExpiredTokenError, match='Token expirado'):
        decode_access_token(expired_token)


def test_decode_token_invalid_secret_raises_error(valid_payload):
    invalid_token = encode(
        payload=valid_payload.model_dump(mode='json'),
        key='chave_secreta_errada',
        algorithm=settings.JWT_ALGORITHM,
    )

    with pytest.raises(InvalidTokenError, match='Token inválido'):
        decode_access_token(invalid_token)


def test_decode_token_malformed_raises_error():
    malformed_token = 'token.invalido.123'

    with pytest.raises(InvalidTokenError, match='Token inválido'):
        decode_access_token(malformed_token)
