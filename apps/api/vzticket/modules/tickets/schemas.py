from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_serializer

from vzticket.core.settings import settings
from vzticket.modules.tickets.model import TicketStatus


class TicketPaymentMethod(str, Enum):
    BALANCE = 'balance'
    PIX = 'pix'


class TicketPurchase(BaseModel):
    quantity: int = Field(default=1, ge=1, le=10, description='Quantidade de ingressos (máximo 10 por compra)')
    payment_method: TicketPaymentMethod = Field(default=TicketPaymentMethod.BALANCE)


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

    model_config = ConfigDict(from_attributes=True)


class TicketEventResponse(BaseModel):
    id: UUID
    title: str
    event_date: datetime
    location_name: str
    city: str
    state: str
    ticket_title: str
    ticket_description: Optional[str] = None

    # Mapeados do Event da ORM, mas ocultados do JSON principal para ir apenas no 'media'
    poster_url: Optional[str] = Field(default=None, exclude=True)
    banner_url: Optional[str] = Field(default=None, exclude=True)
    custom_image_url: Optional[str] = Field(default=None, exclude=True)

    @computed_field
    @property
    def media(self) -> EventMediaResponse:
        return EventMediaResponse(
            poster_url=self.poster_url,
            banner_url=self.banner_url,
            custom_image_url=self.custom_image_url,
        )

    model_config = ConfigDict(from_attributes=True)


class TicketResponse(BaseModel):
    id: UUID
    event_id: UUID
    user_id: UUID
    qr_code_hash: str
    share_token: UUID
    status: TicketStatus
    purchased_at: datetime
    validated_at: Optional[datetime] = None
    event: Optional[TicketEventResponse] = None

    model_config = ConfigDict(from_attributes=True)


class TicketSearch(BaseModel):
    status: Optional[TicketStatus] = Field(default=None)
    page: int = Field(ge=1, default=1, description='Número da página')
    per_page: int = Field(
        ge=1, le=100, default=10, description='Itens por página (máx. 100)'
    )


class PaginatedTicketsResponse(BaseModel):
    items: list[TicketResponse]
    total: int
    page: int
    per_page: int
    pages: int


class TicketPurchaseResponse(BaseModel):
    tickets: list[TicketResponse] = Field(default_factory=list)
    payment_method: TicketPaymentMethod
    payment_token: Optional[str] = Field(
        default=None,
        description='UUID do WalletClaimToken gerado caso o pagamento seja PIX',
    )