from typing import Annotated

from fastapi import Depends, Query

from vzticket.core.database import SessionDep
from vzticket.modules.events.service import EventService
from vzticket.core.libs.tmdb.schemas import TMDBSearchOptions


def get_event_service(session: SessionDep) -> EventService:
    return EventService(session)


EventServiceDep = Annotated[EventService, Depends(get_event_service)]
SearchTMDBOptions = Annotated[TMDBSearchOptions, Query()]
