from typing import Annotated

from fastapi import Depends

from vzticket.core.database import SessionDep
from vzticket.modules.tickets.service import TicketService


def get_ticket_service(session: SessionDep) -> TicketService:
    return TicketService(session)


TicketServiceDep = Annotated[TicketService, Depends(get_ticket_service)]
