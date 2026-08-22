from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from vzticket.modules.tickets.model import Ticket


class TicketRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_many(self, tickets: list[Ticket]) -> list[Ticket]:
        self.session.add_all(tickets)
        await self.session.commit()
        for ticket in tickets:
            await self.session.refresh(ticket)
        return tickets

    async def get_by_id(self, ticket_id: UUID) -> Ticket | None:
        stmt = (
            select(Ticket)
            .options(joinedload(Ticket.event), joinedload(Ticket.user))
            .where(Ticket.id == ticket_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: UUID) -> list[Ticket]:
        stmt = (
            select(Ticket)
            .options(joinedload(Ticket.event))
            .where(Ticket.user_id == user_id)
            .order_by(Ticket.purchased_at.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
