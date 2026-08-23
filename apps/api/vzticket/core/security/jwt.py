from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import ExpiredSignatureError, PyJWTError, decode, encode

from vzticket.core.security.exceptions import ExpiredTokenError, InvalidTokenError
from vzticket.core.security.types import TokenPayload, TokenType
from vzticket.core.settings import settings


def create_access_token(data: TokenPayload) -> str:
    payload = data.model_dump(
        mode='json',
        exclude_unset=True
    )

    exp = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.JWT_TOKEN_EXP_MINUTES
    )

    payload.update({
        'exp': exp,
        'type': TokenType.ACCESS
    })

    access_token = encode(
        payload=payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return access_token


def create_refresh_token(sub: str) -> str:
    exp = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        days=settings.REFRESH_TOKEN_EXP_DAYS
    )

    payload = {
        'sub': str(sub),
        'exp': exp,
        'type': TokenType.REFRESH
    }

    return encode(
        payload=payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )


def decode_access_token(jwt: str) -> TokenPayload:
    try:
        payload = decode(
            jwt=jwt,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        return TokenPayload(**payload)
    except ExpiredSignatureError:
        raise ExpiredTokenError('Token expirado.')
    except PyJWTError:
        raise InvalidTokenError('Token inválido.')


def decode_refresh_token(jwt: str) -> dict:
    try:
        payload = decode(
            jwt=jwt,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        if payload.get('type') != TokenType.REFRESH:
            raise InvalidTokenError('Tipo de token inválido.')

        return payload

    except ExpiredSignatureError:
        raise ExpiredSignatureError('Refresh token expirado.')
    except PyJWTError:
        raise InvalidTokenError('Refresh token inválido.')
