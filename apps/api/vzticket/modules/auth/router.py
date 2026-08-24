from http import HTTPStatus

from fastapi import APIRouter, Request, Response

from vzticket.core.exceptions.swagger import create_error_response
from vzticket.core.settings import settings
from vzticket.modules.auth.dependencies import (
    AuthServiceDep,
    CurrentUserDep,
    LoginFormDataDep,
)
from vzticket.modules.auth.exceptions import InvalidCredentialsError, MissingTokenError
from vzticket.modules.users.exceptions import UserAlreadyExistsError, UserNotFoundError
from vzticket.modules.users.schemas import UserCreate, UserPublic
from vzticket.core.security.exceptions import ExpiredTokenError

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post(
    '/register',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
    responses={
        **create_error_response(
            UserAlreadyExistsError,
            'E-mail já está cadastrado.'
        )
    }
)
async def register(
    data: UserCreate,
    auth_service: AuthServiceDep
):
    return await auth_service.register(data)


@router.post(
    '/login',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
    responses={
        **create_error_response(
            InvalidCredentialsError,
            'E-mail ou senha inválidos.'
        )
    }
)
async def login(
    data: LoginFormDataDep,
    response: Response,
    auth_service: AuthServiceDep
):
    access_token, refresh_token, user = await auth_service.login(data)

    cookies_to_set = [
        (settings.AUTH_COOKIE_NAME, access_token, settings.AUTH_COOKIE_MAX_AGE),
        (settings.REFRESH_COOKIE_NAME, refresh_token, settings.REFRESH_COOKIE_MAX_AGE),
    ]

    for key, value, max_age in cookies_to_set:
        response.set_cookie(
            key=key,
            value=value,
            httponly=True,
            secure=settings.IS_SECURE_COOKIE,
            samesite='none' if settings.IS_SECURE_COOKIE else 'lax',
            max_age=max_age
        )

    return user


@router.post(
    '/logout',
    status_code=HTTPStatus.NO_CONTENT,
    responses={
        **create_error_response(
            MissingTokenError,
            'Token não encontrado.'
        ),
        **create_error_response(
            UserNotFoundError,
            'Usuário não encontrado.'
        ),
    }
)
async def logout(
    response: Response,
    _: CurrentUserDep
):
    cookie_keys = [settings.AUTH_COOKIE_NAME, settings.REFRESH_COOKIE_NAME]

    for key in cookie_keys:
        response.delete_cookie(
            key=key,
            secure=settings.IS_SECURE_COOKIE,
            samesite='none' if settings.IS_SECURE_COOKIE else 'lax',
        )


@router.post(
    '/refresh',
    status_code=HTTPStatus.NO_CONTENT,
    responses={
        **create_error_response(MissingTokenError, 'Refresh token não encontrado.'),
        **create_error_response(ExpiredTokenError, 'Refresh token expirado.'),
    }
)
async def refresh_token(
    req: Request,
    res: Response,
    auth_service: AuthServiceDep
):
    refresh_token = req.cookies.get(settings.REFRESH_COOKIE_NAME)

    if not refresh_token:
        raise MissingTokenError('Refresh token não encontrado.')

    new_access_token = await auth_service.refresh_access_token(refresh_token)

    res.set_cookie(
        key=settings.AUTH_COOKIE_NAME,
        value=new_access_token,
        httponly=True,
        secure=settings.IS_SECURE_COOKIE,
        samesite='none' if settings.IS_SECURE_COOKIE else 'lax',
        max_age=settings.JWT_TOKEN_EXP_MINUTES * 60
    )
