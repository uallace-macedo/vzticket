from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from vzticket.core.database import SessionDep
from vzticket.core.security.jwt import decode_access_token
from vzticket.core.settings import settings
from vzticket.modules.auth.exceptions import MissingTokenError
from vzticket.modules.auth.service import AuthService
from vzticket.modules.users.model import User
from vzticket.modules.users.service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login', auto_error=False)


def get_auth_service(session: SessionDep) -> AuthService:
    return AuthService(session)


async def get_token_from_cookie(
    req: Request
) -> str:
    """Gets HTTPOnly Cookie token"""
    token = req.cookies.get(settings.AUTH_COOKIE_NAME)

    if not token:
        raise MissingTokenError()

    return token


async def get_current_user(
    session: SessionDep,
    token: Annotated[str, Depends(get_token_from_cookie)],
    _: Annotated[str | None, Depends(oauth2_scheme)] = None
) -> User:
    """Decodes the token and returns logged user"""
    payload = decode_access_token(token)
    user_service = UserService(session)
    return await user_service.get_user_by_id(payload.sub)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
LoginFormDataDep = Annotated[OAuth2PasswordRequestForm, Depends()]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
