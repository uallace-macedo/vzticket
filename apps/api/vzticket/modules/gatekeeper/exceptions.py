from http import HTTPStatus

from vzticket.core.exceptions.base import AppError


class TicketAlreadyUsedError(AppError):
    status_code: int = HTTPStatus.BAD_REQUEST
    code: str = 'TICKET_ALREADY_USED'

    def __init__(
        self,
        message: str = 'Ingresso já foi utilizado anteriormente',
    ) -> None:
        super().__init__(message)


class TicketNotForThisEventError(AppError):
    status_code: int = HTTPStatus.BAD_REQUEST
    code: str = 'TICKET_NOT_FOR_THIS_EVENT'

    def __init__(
        self, message: str = 'Este ingresso não pertence a este evento'
    ) -> None:
        super().__init__(message)
