from http import HTTPStatus

from vzticket.core.exceptions.base import AppError


class TokenNotFoundError(AppError):
    status_code: int = HTTPStatus.NOT_FOUND
    code: str = 'TOKEN_NOT_FOUND'

    def __init__(self, message: str = 'Token de resgate não encontrado') -> None:
        super().__init__(message)


class TokenAlreadyClaimedError(AppError):
    status_code: int = HTTPStatus.CONFLICT
    code: str = 'TOKEN_ALREADY_CLAIMED'

    def __init__(self, message: str = 'Este QR Code/Link já foi resgatado') -> None:
        super().__init__(message)


class TokenExpiredError(AppError):
    status_code: int = HTTPStatus.BAD_REQUEST
    code: str = 'TOKEN_EXPIRED'

    def __init__(self, message: str = 'Este QR Code/Link expirou') -> None:
        super().__init__(message)
