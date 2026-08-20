from http import HTTPStatus

from vzticket.core.exceptions.base import AppError


class UserNotFoundError(AppError):
    status_code = HTTPStatus.NOT_FOUND
    code = 'USER_NOT_FOUND'

    def __init__(self, message: str = 'Usuário não encontrado.') -> None:
        super().__init__(message)


class UserAlreadyExistsError(AppError):
    status_code = HTTPStatus.CONFLICT
    code = 'USER_ALREADY_EXISTS'

    def __init__(self, message: str = 'Este email já está cadastrado.') -> None:
        super().__init__(message)
