from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import ExpiredSignatureError, PyJWTError, decode, encode

from vzticket.core.security.exceptions import ExpiredTokenError, InvalidTokenError
from vzticket.core.security.types import TokenPayload
from vzticket.core.settings import settings


def create_access_token(data: TokenPayload) -> str:
    payload = data.model_dump(
        mode='json',
        exclude_unset=True
    )

    exp = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.JWT_TOKEN_EXP_MINUTES
    )

    payload.update({'exp': exp})

    access_token = encode(
        payload=payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return access_token


def decode_access_token(jwt: str) -> TokenPayload:
    try:
        payload = decode(
            jwt=jwt,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        return TokenPayload(**payload)
    except ExpiredSignatureError:
        raise ExpiredTokenError('Token expirado')
    except PyJWTError:
        raise InvalidTokenError('Token inválido')
