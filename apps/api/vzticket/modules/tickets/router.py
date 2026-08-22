from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter

from vzticket.core.exceptions.swagger import create_error_response
from vzticket.modules.auth.dependencies import CurrentUserDep
from vzticket.modules.events.exceptions import EventNotFoundError
from vzticket.modules.tickets.dependencies import TicketServiceDep
from vzticket.modules.tickets.exceptions import (
    EventNotActiveError,
    EventSalesEndedError,
    EventSalesNotStartedError,
    InsufficientBalanceForTicketError,
    InsufficientTicketsError,
    TicketNotFoundError,
)
from vzticket.modules.tickets.schemas import (
    TicketPurchase,
    TicketPurchaseResponse,
    TicketResponse,
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
    response_model=list[TicketResponse],
)
async def get_my_tickets(
    ticket_service: TicketServiceDep,
    current_user: CurrentUserDep,
):
    return await ticket_service.get_user_tickets(current_user.id)


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
