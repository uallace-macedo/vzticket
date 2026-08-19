from http import HTTPStatus

from verzel.core.exceptions.base import AppError


class InvalidCredentialsError(AppError):
    status_code = HTTPStatus.UNAUTHORIZED
    code = 'INVALID_CREDENTIALS'

    def __init__(self, message: str = 'E-mail ou senha inválidos.') -> None:
        super().__init__(message)


class MissingTokenError(AppError):
    status_code = HTTPStatus.UNAUTHORIZED
    code = 'MISSING_TOKEN'

    def __init__(self, message: str = 'Token de acesso inexistente.') -> None:
        super().__init__(message)
