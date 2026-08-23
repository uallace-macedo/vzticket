from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter

from vzticket.core.exceptions.swagger import create_error_response
from vzticket.modules.auth.dependencies import CurrentUserDep
from vzticket.modules.events.exceptions import EventNotFoundError
from vzticket.modules.tickets.dependencies import TicketServiceDep, TicketSearchDep
from vzticket.modules.tickets.exceptions import (
    EventNotActiveError,
    EventSalesEndedError,
    EventSalesNotStartedError,
    InsufficientBalanceForTicketError,
    InsufficientTicketsError,
    TicketNotFoundError,
    TicketRefundWindowClosedError,
    TicketRefund7DaysExpiredError,
    TicketAlreadyCancelledError
)
from vzticket.modules.tickets.schemas import (
    TicketPurchase,
    TicketPurchaseResponse,
    TicketResponse,
    PaginatedTicketsResponse
)

router = APIRouter(prefix='/tickets', tags=['Tickets'])


@router.post(
    '/events/{event_id}/purchase',
    status_code=HTTPStatus.CREATED,
    response_model=TicketPurchaseResponse,
    responses={
        **create_error_response(
            EventNotFoundError, 'Evento não encontrado.'
        ),
        **create_error_response(
            EventNotActiveError, 'O evento não está ativo para vendas.'
        ),
        **create_error_response(
            EventSalesNotStartedError,
            'As vendas para este evento ainda não começaram.',
        ),
        **create_error_response(
            EventSalesEndedError, 'As vendas para este evento já foram encerradas.'
        ),
        **create_error_response(
            InsufficientTicketsError,
            'Quantidade de ingressos solicitada indisponível.',
        ),
        **create_error_response(
            InsufficientBalanceForTicketError,
            'Saldo insuficiente para realizar a compra dos ingressos.',
        ),
    },
)
async def purchase_tickets(
    event_id: UUID,
    data: TicketPurchase,
    ticket_service: TicketServiceDep,
    current_user: CurrentUserDep,
):
    return await ticket_service.purchase_tickets(event_id, current_user, data)


@router.get(
    '/my-tickets',
    status_code=HTTPStatus.OK,
    response_model=PaginatedTicketsResponse,
)
async def get_my_tickets(
    ticket_service: TicketServiceDep,
    params: TicketSearchDep,
    current_user: CurrentUserDep,
):
    return await ticket_service.get_user_tickets(current_user.id, params)


@router.get(
    '/{ticket_id}',
    status_code=HTTPStatus.OK,
    response_model=TicketResponse,
    responses={
        **create_error_response(
            TicketNotFoundError, 'Ingresso não encontrado.'
        ),
    },
)
async def get_ticket_by_id(
    ticket_id: UUID,
    ticket_service: TicketServiceDep,
    _: CurrentUserDep,
):
    return await ticket_service.get_ticket_by_id(ticket_id)


@router.patch(
    '/{ticket_id}/cancel',
    response_model=TicketResponse,
    status_code=HTTPStatus.OK,
    summary='Cancelar ingresso e solicitar reembolso',
    responses={
        **create_error_response(
            TicketNotFoundError, 'Ingresso não encontrado.'
        ),
        **create_error_response(
            TicketAlreadyCancelledError, 'Ingresso já cancelado ou utilizado.'
        ),
        **create_error_response(
            TicketRefund7DaysExpiredError, 'Prazo legal de 7 dias expirado.'
        ),
        **create_error_response(
            TicketRefundWindowClosedError, 'Prazo limite do evento expirado (< 24h).'
        ),
    },
)
async def cancel_ticket(
    ticket_id: UUID,
    current_user: CurrentUserDep,
    ticket_service: TicketServiceDep,
) -> TicketResponse:
    cancelled_ticket = await ticket_service.cancel_ticket(
        user_id=current_user.id,
        ticket_id=ticket_id,
    )

    return TicketResponse.model_validate(cancelled_ticket)
