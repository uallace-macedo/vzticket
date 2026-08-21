from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.core.libs.tmdb.client import TMDBClient
from vzticket.core.libs.tmdb.schemas import TMDBSearchOptions, TMDBSearchResponse
from vzticket.modules.events.exceptions import EventNotFoundError
from vzticket.modules.events.model import Event
from vzticket.modules.events.repository import EventRepository
from vzticket.modules.events.schemas import EventCreate, EventsSearch


class EventService:
    def __init__(self, session: AsyncSession) -> None:
        self.tmdb_client = TMDBClient()
        self.event_repository = EventRepository(session)

    async def search_tmdb(self, options: TMDBSearchOptions) -> TMDBSearchResponse:
        """Uses TMDB Lib to search movies, tv shows and people"""
        return await self.tmdb_client.search(
            options.title,
            options.page
        )

    async def create(self, data: EventCreate) -> Event:
        event = Event(
            **data.model_dump(mode='python', exclude_unset=True)
        )

        return await self.event_repository.create(event)

    async def get_by_id(self, event_id: UUID) -> Event:
        event = await self.event_repository.get_by_id(event_id)
        if not event:
            raise EventNotFoundError()

        return event

    async def search_events(self, options: EventsSearch) -> list[Event]:
        return await self.event_repository.search_events(
            title=options.title,
            limit=options.limit,
            offset=options.offset
        )
