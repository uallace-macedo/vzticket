from http import HTTPStatus

from vzticket.core.exceptions.base import AppError


class InvalidTransactionError(AppError):
    status_code = HTTPStatus.BAD_REQUEST
    code = 'INVALID_TRANSACTION'

    def __init__(self, message: str = 'Transação inválida.') -> None:
        super().__init__(message)
