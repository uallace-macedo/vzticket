from typing import Annotated, Optional

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from vzticket.core.database import SessionDep
from vzticket.core.security.jwt import decode_access_token
from vzticket.core.settings import settings
from vzticket.modules.auth.exceptions import MissingTokenError, NotAllowedError
from vzticket.modules.auth.service import AuthService
from vzticket.modules.users.model import User, UserRole
from vzticket.modules.users.service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login', auto_error=False)


def get_auth_service(session: SessionDep) -> AuthService:
    return AuthService(session)


async def get_token_from_cookie(
    req: Request
) -> str | None:
    return req.cookies.get(settings.AUTH_COOKIE_NAME)


async def get_optional_current_user(
    session: SessionDep,
    token: Annotated[str | None, Depends(get_token_from_cookie)],
    _: Annotated[str | None, Depends(oauth2_scheme)] = None
) -> Optional[User]:
    if not token:
        return None

    try:
        payload = decode_access_token(token)
        user_service = UserService(session)
        return await user_service.get_user_by_id(payload.sub)
    except Exception:
        return None


async def get_current_user(
    user: Annotated[Optional[User], Depends(get_optional_current_user)]
) -> User:
    if not user:
        raise MissingTokenError()
    
    return user


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
LoginFormDataDep = Annotated[OAuth2PasswordRequestForm, Depends()]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
OptionalCurrentUserDep = Annotated[
    Optional[User], Depends(get_optional_current_user)
]


class RoleChecker:
    def __init__(self, allowed_routes: list[UserRole]) -> None:
        self.allowed_routes = allowed_routes

    def __call__(self, current_user: CurrentUserDep) -> User:
        if current_user.role not in self.allowed_routes:
            raise NotAllowedError()

        return current_user
