from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from vzticket.modules.events.model import Event, EventStatus
from vzticket.modules.events.schemas import EventsSearch


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

    async def search_events(self, options: EventsSearch) -> list[Event]:
        stmt = (
            select(Event)
            .options(joinedload(Event.organizer))
            .where(Event.status == EventStatus.ACTIVE)
        )

        if options.title:
            stmt = stmt.where(Event.title.ilike(f'%{options.title}%'))

        if options.city:
            stmt = stmt.where(Event.city_slug.ilike(f'%{options.city}%'))

        if options.state:
            stmt = stmt.where(Event.state.ilike(f'%{options.state}%'))

        stmt = stmt.order_by(Event.event_date.asc()).limit(options.limit).offset(options.offset)
        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def get_by_organizer_id(self, organizer_id: UUID) -> list[Event]:
        stmt = (
            select(Event)
            .options(joinedload(Event.organizer))
            .where(Event.organizer_id == organizer_id)
            .order_by(Event.created_at.desc())
        )
        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def update(self, event: Event) -> Event:
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event
