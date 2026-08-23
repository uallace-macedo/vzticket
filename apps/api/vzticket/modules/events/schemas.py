from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_serializer,
    field_validator,
)

from vzticket.core.settings import settings
from vzticket.modules.events.model import EventStatus
from vzticket.modules.events.utils import slugify_city


class PaymentMethod(str, Enum):
    BALANCE = 'balance'
    PIX = 'pix'


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
    title: str = Field(min_length=3, max_length=150)
    description: str = Field(min_length=10)

    available_tickets: int = Field(ge=1)
    ticket_price: Decimal = Field(ge=Decimal('0.00'), decimal_places=2)
    ticket_title: str = Field(default='Ingresso Geral', max_length=100)
    ticket_description: Optional[str] = Field(default=None)

    event_date: datetime
    sales_start_at: Optional[datetime] = Field(default=None)
    sales_end_at: Optional[datetime] = Field(default=None)

    location_name: str = Field(max_length=150)
    cep: str = Field(min_length=9, max_length=9, pattern=r'^\d{5}-\d{3}$')
    address: str = Field(max_length=255)
    number: str = Field(max_length=20)
    neighborhood: str = Field(max_length=100)
    city: str = Field(max_length=100)
    state: str = Field(min_length=2, max_length=2)
    complement: Optional[str] = Field(default=None)

    poster_url: Optional[str] = Field(default=None)
    banner_url: Optional[str] = Field(default=None)
    custom_image_url: Optional[str] = Field(default=None)
    maps_url: Optional[str] = Field(default=None)

    payment_method: PaymentMethod = Field(default=PaymentMethod.BALANCE)

    @field_validator('event_date')
    @classmethod
    def validate_future_date(cls, v: datetime) -> datetime:
        now = datetime.now(timezone.utc)
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        if v <= now:
            raise ValueError('A data do evento deve ser no futuro')
        return v

    @field_validator('state')
    @classmethod
    def normalize_state(cls, v: str) -> str:
        return v.upper()


class OrganizerResponse(BaseModel):
    id: UUID
    name: str
    email: str
    image_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class EventLocationResponse(BaseModel):
    name: str
    cep: str
    address: str
    number: str
    neighborhood: str
    city: str
    state: str
    complement: Optional[str] = None
    maps_url: Optional[str] = None


class EventMediaResponse(BaseModel):
    poster_url: Optional[str] = None
    banner_url: Optional[str] = None
    custom_image_url: Optional[str] = None

    @field_serializer('poster_url', 'banner_url')
    @classmethod
    def serialize_tmdb_url(cls, v: Optional[str]) -> Optional[str]:
        if v and v.startswith('/'):
            return f'{settings.TMDB_IMAGE_BASE_URL}{v}'
        return v


class TicketInfoResponse(BaseModel):
    title: str
    description: Optional[str] = None
    available_tickets: int
    ticket_price: float
    service_fee: float

    @computed_field
    def total_price(self) -> float:
        return float(Decimal(str(self.ticket_price)) + Decimal(str(self.service_fee)))

    @field_serializer('ticket_price', 'service_fee')
    def serialize_decimal_to_float(self, v: float) -> float:
        return float(v)


class EventResponse(BaseModel):
    id: UUID
    title: str
    description: str
    status: EventStatus

    event_date: datetime
    sales_start_at: Optional[datetime] = None
    sales_end_at: Optional[datetime] = None

    ticket_info: TicketInfoResponse
    location: EventLocationResponse
    media: EventMediaResponse
    organizer: OrganizerResponse

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EventCreatedResponse(BaseModel):
    event: EventResponse
    payment_method: PaymentMethod
    payment_token: Optional[str] = Field(
        default=None,
        description='UUID do WalletClaimToken gerado caso o pagamento seja PIX',
    )


class EventUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=150)
    description: Optional[str] = Field(default=None, min_length=10)

    available_tickets: Optional[int] = Field(default=None, ge=1)
    ticket_price: Optional[Decimal] = Field(default=None, ge=Decimal('0.00'), decimal_places=2)
    ticket_title: Optional[str] = Field(default=None, max_length=100)
    ticket_description: Optional[str] = Field(default=None)

    event_date: Optional[datetime] = Field(default=None)
    sales_start_at: Optional[datetime] = Field(default=None)
    sales_end_at: Optional[datetime] = Field(default=None)

    location_name: Optional[str] = Field(default=None, max_length=150)
    cep: Optional[str] = Field(default=None, min_length=9, max_length=9, pattern=r'^\d{5}-\d{3}$')
    address: Optional[str] = Field(default=None, max_length=255)
    number: Optional[str] = Field(default=None, max_length=20)
    neighborhood: Optional[str] = Field(default=None, max_length=100)
    city: Optional[str] = Field(default=None, max_length=100)
    state: Optional[str] = Field(default=None, min_length=2, max_length=2)
    complement: Optional[str] = Field(default=None)

    poster_url: Optional[str] = Field(default=None)
    banner_url: Optional[str] = Field(default=None)
    custom_image_url: Optional[str] = Field(default=None)
    maps_url: Optional[str] = Field(default=None)

    @field_validator('event_date')
    @classmethod
    def validate_future_date(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is not None:
            now = datetime.now(timezone.utc)
            if v.tzinfo is None:
                v = v.replace(tzinfo=timezone.utc)
            if v <= now:
                raise ValueError('A data do evento deve ser no futuro')
        return v

    @field_validator('state')
    @classmethod
    def normalize_state(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return v.upper()
        return v


class MyEventsSearch(BaseModel):
    status: Optional[EventStatus] = Field(default=None)
    page: int = Field(ge=1, default=1, description='Número da página')
    per_page: int = Field(
        ge=1, le=100, default=10, description='Itens por página (máx. 100)'
    )


class PaginatedEventsResponse(BaseModel):
    items: list[EventResponse]
    total: int
    page: int
    per_page: int
    pages: int
