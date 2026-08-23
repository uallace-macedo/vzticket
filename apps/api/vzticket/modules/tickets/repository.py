from math import ceil
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from vzticket.modules.tickets.model import Ticket
from vzticket.modules.tickets.schemas import TicketSearch


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

    async def get_by_user_id(
        self,
        user_id: UUID,
        params: TicketSearch,
    ) -> tuple[list[Ticket], int, int]:
        base_stmt = select(Ticket).where(Ticket.user_id == user_id)

        if params.status:
            base_stmt = base_stmt.where(Ticket.status == params.status)

        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar_one()

        offset = (params.page - 1) * params.per_page
        pages = ceil(total / params.per_page) if total > 0 else 1

        stmt = (
            base_stmt
            .options(joinedload(Ticket.event))
            .order_by(Ticket.purchased_at.desc())
            .offset(offset)
            .limit(params.per_page)
        )

        result = await self.session.execute(stmt)
        tickets = result.scalars().all()

        return list(tickets), total, pages
