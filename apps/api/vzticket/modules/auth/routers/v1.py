"""HTTP routes for the auth module."""

from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.core.database import get_db
from vzticket.core.config import settings
from vzticket.core.exceptions.swagger import create_error_response
from vzticket.modules.auth.deps import get_current_user, get_auth_service
from vzticket.modules.auth.exceptions import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    InvalidTokenError,
    UnauthorizedError,
)
from vzticket.modules.auth.models import User
from vzticket.modules.auth.repository import UserRepository
from vzticket.modules.auth.service import AuthService
from vzticket.modules.auth.schemas import (
    MessageResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)
from vzticket.modules.auth.security import create_access_token, create_refresh_token
from vzticket.modules.auth.service import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])

ACCESS_COOKIE = settings.access_token_cookie_name
REFRESH_COOKIE = settings.refresh_token_cookie_name


def _set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    response.set_cookie(
        key=ACCESS_COOKIE,
        value=access_token,
        httponly=True,
        secure=False,
        samesite='lax',
        path='/',
    )
    response.set_cookie(
        key=REFRESH_COOKIE,
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite='lax',
        path='/',
    )


def _clear_auth_cookies(response: Response) -> None:
    response.delete_cookie(key=ACCESS_COOKIE, path='/')
    response.delete_cookie(key=REFRESH_COOKIE, path='/')


@router.post(
    '/register',
    response_model=UserResponse,
    status_code=201,
    responses={
        409: create_error_response(EmailAlreadyRegisteredError, 'E-mail já cadastrado')
    },
)
async def register(
    data: UserRegister,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> User:
    """Register a new user."""
    return await service.register_user(data)


@router.post(
    '/login',
    response_model=UserResponse,
    responses={
        401: create_error_response(InvalidCredentialsError, 'Credenciais inválidas')
    },
)
async def login(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> User:
    """Authenticate a user and set HTTP-Only auth cookies."""
    user = await service.authenticate_user(data.username, data.password)
    _set_auth_cookies(
        response,
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )
    return user


@router.post(
    '/refresh',
    response_model=MessageResponse,
    responses={
        401: create_error_response(InvalidTokenError, 'Token inválido ou expirado')
    },
)
async def refresh(
    response: Response,
    service: Annotated[AuthService, Depends(get_auth_service)],
    refresh_token: Annotated[str | None, Cookie(alias=REFRESH_COOKIE)] = None,
) -> MessageResponse:
    """Refresh the access token using the refresh cookie."""
    if refresh_token is None:
        raise InvalidTokenError

    tokens = await service.refresh_tokens(refresh_token)
    _set_auth_cookies(
        response,
        access_token=tokens['access_token'],
        refresh_token=tokens['refresh_token'],
    )
    return MessageResponse(message='Tokens atualizados com sucesso.')


@router.post(
    '/logout',
    response_model=MessageResponse,
    responses={
        401: create_error_response(UnauthorizedError, 'Autenticação necessária')
    },
)
async def logout(
    response: Response,
    _: Annotated[User, Depends(get_current_user)],
) -> MessageResponse:
    """Clear the HTTP-Only auth cookies."""
    _clear_auth_cookies(response)
    return MessageResponse(message='Logout realizado com sucesso.')


@router.get(
    '/me',
    response_model=UserResponse,
    responses={
        401: create_error_response(UnauthorizedError, 'Autenticação necessária')
    },
)
async def me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Return the currently authenticated user."""
    return current_user
