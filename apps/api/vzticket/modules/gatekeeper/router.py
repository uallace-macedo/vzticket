from http import HTTPStatus

from fastapi import APIRouter, Depends

from vzticket.core.exceptions.swagger import create_error_response
from vzticket.modules.auth.dependencies import CurrentUserDep, RoleChecker
from vzticket.modules.gatekeeper.dependencies import GatekeeperServiceDep
from vzticket.modules.gatekeeper.exceptions import (
    TicketAlreadyUsedError,
    TicketNotForThisEventError,
)
from vzticket.modules.gatekeeper.schemas import (
    ValidateTicketRequest,
    ValidateTicketResponse,
)
from vzticket.modules.tickets.exceptions import (
    TicketAlreadyCancelledError,
    TicketNotFoundError,
)
from vzticket.modules.users.model import UserRole

router = APIRouter(prefix='/gatekeeper', tags=['Gatekeeper'])

gatekeeper_or_organizer = Depends(
    RoleChecker(allowed_routes=[UserRole.GATEKEEPER, UserRole.ORGANIZER])
)


@router.post(
    '/validate-ticket',
    status_code=HTTPStatus.OK,
    response_model=ValidateTicketResponse,
    dependencies=[gatekeeper_or_organizer],
    responses={
        **create_error_response(
            TicketNotFoundError, 'Ingresso não encontrado.'
        ),
        **create_error_response(
            TicketAlreadyUsedError, 'Ingresso já utilizado anteriormente.'
        ),
        **create_error_response(
            TicketNotForThisEventError,
            'Este ingresso não pertence a este evento.',
        ),
        **create_error_response(
            TicketAlreadyCancelledError, 'Ingresso cancelado.'
        ),
    },
)
async def validate_ticket(
    gatekeeper_service: GatekeeperServiceDep,
    data: ValidateTicketRequest,
    current_user: CurrentUserDep,
):
    """Valida a entrada do evento lendo a hash do QR Code (Portaria / Organizador)."""
    return await gatekeeper_service.validate_ticket(data, current_user.id)
