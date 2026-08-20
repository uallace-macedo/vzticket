from typing import Annotated

from fastapi import Depends

from vzticket.core.database import SessionDep
from vzticket.modules.events.service import EventService


def get_event_service(session: SessionDep) -> EventService:
    return EventService(session)


EventServiceDep = Annotated[EventService, Depends(get_event_service)]
