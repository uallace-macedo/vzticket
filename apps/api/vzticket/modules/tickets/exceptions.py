from http import HTTPStatus

from vzticket.core.exceptions.base import AppError


class EventNotActiveError(AppError):
    status_code: int = HTTPStatus.BAD_REQUEST
    code: str = 'EVENT_NOT_ACTIVE'

    def __init__(self, message: str = 'O evento não está ativo para vendas.') -> None:
        super().__init__(message)


class EventSalesNotStartedError(AppError):
    status_code: int = HTTPStatus.BAD_REQUEST
    code: str = 'EVENT_SALES_NOT_STARTED'

    def __init__(
        self,
        message: str = 'As vendas para este evento ainda não começaram.'
    ) -> None:
        super().__init__(message)


class EventSalesEndedError(AppError):
    status_code: int = HTTPStatus.BAD_REQUEST
    code: str = 'EVENT_SALES_ENDED'

    def __init__(
        self,
        message: str = 'As vendas para este evento já foram encerradas.'
    ) -> None:
        super().__init__(message)


class InsufficientTicketsError(AppError):
    status_code: int = HTTPStatus.BAD_REQUEST
    code: str = 'INSUFFICIENT_TICKETS'

    def __init__(
        self,
        message: str = 'Quantidade de ingressos solicitada indisponível.'
    ) -> None:
        super().__init__(message)


class InsufficientBalanceForTicketError(AppError):
    status_code: int = HTTPStatus.PAYMENT_REQUIRED
    code: str = 'INSUFFICIENT_BALANCE_FOR_TICKET'

    def __init__(
        self, message: str = 'Saldo insuficiente para realizar a compra dos ingressos.'
    ) -> None:
        super().__init__(message)


class TicketNotFoundError(AppError):
    status_code: int = HTTPStatus.NOT_FOUND
    code: str = 'TICKET_NOT_FOUND'

    def __init__(self, message: str = 'Ingresso não encontrado.') -> None:
        super().__init__(message)


class TicketAlreadyCancelledError(AppError):
    status_code: int = HTTPStatus.BAD_REQUEST
    code: str = 'TICKET_ALREADY_CANCELLED'

    def __init__(self, message: str = 'Este ingresso já foi cancelado ou utilizado.') -> None:
        super().__init__(message)


class TicketRefund7DaysExpiredError(AppError):
    status_code: int = HTTPStatus.BAD_REQUEST
    code: str = 'TICKET_REFUND_7_DAYS_EXPIRED'

    def __init__(self, message: str = 'O prazo legal de 7 dias para cancelamento do ingresso expirou.') -> None:
        super().__init__(message)


class TicketRefundWindowClosedError(AppError):
    status_code: int = HTTPStatus.BAD_REQUEST
    code: str = 'TICKET_REFUND_WINDOW_CLOSED'

    def __init__(self, message: str = 'Solicitações de reembolso não são permitidas com menos de 24h para o início do evento.') -> None:
        super().__init__(message)
