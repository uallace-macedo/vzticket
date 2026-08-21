from http import HTTPStatus

from vzticket.core.exceptions.base import AppError


class EventNotFoundError(AppError):
    status_code: int = HTTPStatus.NOT_FOUND
    code: str = 'EVENT_NOT_FOUND'

    def __init__(self, message: str = 'Evento não encontrado') -> None:
        super().__init__(message)
