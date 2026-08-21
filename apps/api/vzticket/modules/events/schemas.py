from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class EventsSearch(BaseModel):
    title: Optional[str] = Field(default=None)
    limit: Optional[int] = Field(ge=1, default=10)
    offset: Optional[int] = Field(ge=0, default=0)


class EventCreate(BaseModel):
    organizer_id: UUID
    title: str
    description: str

    available_tickets: int = Field(ge=1)
    ticket_price: float = Field(ge=0)

    location: str
    location_url: Optional[str] = Field(default=None)
    event_date: datetime

    poster_url: Optional[str] = Field(default=None)
    banner_url: Optional[str] = Field(default=None)


class OrganizerResponse(BaseModel):
    id: UUID
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class EventResponse(BaseModel):
    id: UUID
    title: str
    description: str
    available_tickets: int
    ticket_price: float
    location: str
    location_url: Optional[str] = None
    event_date: datetime
    poster_url: Optional[str] = None
    banner_url: Optional[str] = None

    organizer: OrganizerResponse

    model_config = ConfigDict(from_attributes=True)
