from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from vzticket.modules.events.model import Event


class EventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, event: Event) -> Event:
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)

        return event

    async def get_by_id(self, event_id: UUID) -> Event | None:
        stmt = (
            select(Event)
            .options(joinedload(Event.organizer))
            .where(Event.id == event_id)
        )
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def search_events(
        self,
        title: str | None,
        limit: int,
        offset: int
    ) -> list[Event]:
        stmt = (
            select(Event)
            .options(joinedload(Event.organizer))
        )

        if title:
            stmt = stmt.where(Event.title.ilike(f'%{title}%'))

        stmt = stmt.limit(limit).offset(offset)
        result = await self.session.execute(stmt)

        return list(result.scalars().all())
