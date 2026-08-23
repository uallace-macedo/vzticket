from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from vzticket.modules.tickets.model import Ticket


class GatekeeperRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_ticket_for_validation(
        self, qr_code_hash: str
    ) -> Optional[Ticket]:
        stmt = (
            select(Ticket)
            .options(
                joinedload(Ticket.user, innerjoin=True),
                joinedload(Ticket.event, innerjoin=True),
            )
            .where(Ticket.qr_code_hash == qr_code_hash)
            .with_for_update()
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def save(self, ticket: Ticket) -> Ticket:
        self.session.add(ticket)
        await self.session.commit()
        await self.session.refresh(ticket)
        return ticket
