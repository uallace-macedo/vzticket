from http import HTTPStatus

from fastapi import APIRouter, Response

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
    token, user = await auth_service.login(data)
    response.set_cookie(
        key=settings.AUTH_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.IS_SECURE_COOKIE,
        samesite='none' if settings.IS_SECURE_COOKIE else 'lax',
        max_age=settings.AUTH_COOKIE_MAX_AGE
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
    response.delete_cookie(
        key=settings.AUTH_COOKIE_NAME,
        secure=settings.IS_SECURE_COOKIE,
        samesite='none' if settings.IS_SECURE_COOKIE else 'lax',
    )
