from http import HTTPStatus

from vzticket.core.exceptions.base import AppError


class EventNotFoundError(AppError):
    status_code: int = HTTPStatus.NOT_FOUND
    code: str = 'EVENT_NOT_FOUND'

    def __init__(self, message: str = 'Evento não encontrado') -> None:
        super().__init__(message)


class InsufficientBalanceForFeeError(AppError):
    status_code: int = HTTPStatus.PAYMENT_REQUIRED
    code: str = 'INSUFFICIENT_BALANCE_FOR_FEE'

    def __init__(
        self, message: str = 'Saldo insuficiente para pagar a taxa de criação do evento'
    ) -> None:
        super().__init__(message)


class EventAlreadyActiveError(AppError):
    status_code: int = HTTPStatus.CONFLICT
    code: str = 'EVENT_ALREADY_ACTIVE'

    def __init__(
        self, message: str = 'Este evento já está ativo e com a taxa paga'
    ) -> None:
        super().__init__(message)
