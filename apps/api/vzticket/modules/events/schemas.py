from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator

from vzticket.core.settings import settings
from vzticket.modules.events.utils import slugify_city


class EventsSearch(BaseModel):
    title: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None, max_length=2, min_length=2)
    limit: Optional[int] = Field(ge=1, default=10)
    offset: Optional[int] = Field(ge=0, default=0)

    @field_validator('city')
    def normalize_city(cls, v: Optional[str]) -> Optional[str]:
        if v:
            return slugify_city(v)
        return v

    @field_validator('state')
    def normalize_state(cls, v: Optional[str]) -> Optional[str]:
        if v:
            return v.upper()
        return v


class EventCreate(BaseModel):
    organizer_id: UUID

    title: str
    description: str
    available_tickets: int = Field(ge=1)
    ticket_price: Decimal = Field(ge=Decimal('0.00'), decimal_places=2)
    event_date: datetime = Field(gt=datetime.now(timezone.utc))

    location_name: str = Field(max_length=150)
    cep: str = Field(min_length=9, max_length=9, pattern=r'^\d{5}-\d{3}$')
    address: str = Field(max_length=255)
    number: str = Field(max_length=20)
    neighborhood: str = Field(max_length=100)
    city: str = Field(max_length=100)
    state: str = Field(min_length=2, max_length=2)

    poster_url: Optional[str] = Field(default=None)
    banner_url: Optional[str] = Field(default=None)
    complement: Optional[str] = Field(default=None)
    custom_image_url: Optional[str] = Field(default=None)
    maps_url: Optional[str] = Field(default=None)

    @field_validator('state')
    @classmethod
    def normalize_state(cls, v: str) -> str:
        return v.upper()


class OrganizerResponse(BaseModel):
    id: UUID
    name: str
    email: str
    image_url: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class EventResponse(BaseModel):
    id: UUID

    title: str
    description: str
    available_tickets: int
    ticket_price: float
    event_date: datetime

    location_name: str
    cep: str
    address: str
    number: str
    neighborhood: str
    city: str
    state: str
    complement: Optional[str]
    maps_url: Optional[str]

    poster_url: Optional[str]
    banner_url: Optional[str]
    custom_image_url: Optional[str]

    organizer: OrganizerResponse

    @field_serializer('poster_url', 'banner_url')
    @classmethod
    def serialize_tmdb_url(cls, v: Optional[str]) -> Optional[str]:
        if v and v.startswith('/'):
            return f'{settings.TMDB_IMAGE_BASE_URL}{v}'
        return v

    model_config = ConfigDict(from_attributes=True)
