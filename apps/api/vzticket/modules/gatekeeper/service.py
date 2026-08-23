from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.modules.gatekeeper.exceptions import (
    TicketAlreadyUsedError,
    TicketNotForThisEventError,
)
from vzticket.modules.gatekeeper.repository import GatekeeperRepository
from vzticket.modules.gatekeeper.schemas import (
    ValidateTicketRequest,
    ValidateTicketResponse,
)
from vzticket.modules.tickets.exceptions import (
    TicketAlreadyCancelledError,
    TicketNotFoundError,
)
from vzticket.modules.tickets.model import TicketStatus


class GatekeeperService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = GatekeeperRepository(session)

    async def validate_ticket(
        self, data: ValidateTicketRequest, gatekeeper_id: UUID
    ) -> ValidateTicketResponse:
        ticket = await self.repository.get_ticket_for_validation(
            data.qr_code_hash
        )

        if not ticket:
            raise TicketNotFoundError()

        if ticket.event_id != data.event_id:
            raise TicketNotForThisEventError()

        if ticket.status == TicketStatus.CANCELLED:
            raise TicketAlreadyCancelledError()

        if ticket.validated_at is not None or ticket.status == TicketStatus.USED:
            formatted_time = (
                ticket.validated_at.strftime('%H:%M:%S')
                if ticket.validated_at
                else ''
            )
            msg = (
                f'Ingresso já utilizado às {formatted_time}'
                if formatted_time
                else 'Ingresso já foi utilizado'
            )
            raise TicketAlreadyUsedError(message=msg)

        now = datetime.now(timezone.utc)
        event_date = ticket.event.event_date.replace(tzinfo=timezone.utc) if ticket.event.event_date.tzinfo is None else ticket.event.event_date

        if now.date() < event_date.date():
            raise TicketNotForThisEventError(message='A portaria para este evento ainda não está aberta!')

        ticket.validated_at = now
        ticket.status = TicketStatus.USED

        await self.repository.save(ticket)

        return ValidateTicketResponse(
            ticket_id=ticket.id,
            event_id=ticket.event_id,
            buyer_name=ticket.user.name,
            buyer_email=ticket.user.email,
            status=ticket.status.value,
            validated_at=now,
        )
