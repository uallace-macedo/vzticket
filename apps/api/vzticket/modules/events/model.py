import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from vzticket.core.database import table_registry

if TYPE_CHECKING:
    from vzticket.modules.tickets.model import Ticket
    from vzticket.modules.users.model import User
    from vzticket.modules.events_payout.model import EventPayout


class EventStatus(str, Enum):
    PENDING_FEE = 'pending_fee'
    ACTIVE = 'active'
    CANCELLED = 'cancelled'
    FINISHED = 'finished'


@table_registry.mapped_as_dataclass
class Event:
    __tablename__ = 'tb_events'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False,
        primary_key=True,
        nullable=False,
        default_factory=uuid.uuid4
    )

    organizer_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('tb_users.id'), nullable=False, index=True
    )

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    event_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    available_tickets: Mapped[int] = mapped_column(nullable=False)
    ticket_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    location_name: Mapped[str] = mapped_column(String(150), nullable=False)
    cep: Mapped[str] = mapped_column(String(9), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    number: Mapped[str] = mapped_column(String(20), nullable=False)
    neighborhood: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    city_slug: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    state: Mapped[str] = mapped_column(String(2), nullable=False)

    status: Mapped[EventStatus] = mapped_column(
        SQLEnum(EventStatus, native_enum=False),
        default=EventStatus.PENDING_FEE,
        nullable=False,
    )
    service_fee: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), default=Decimal('2.80'), nullable=False
    )
    ticket_title: Mapped[str] = mapped_column(
        String(100), default='Ingresso Geral', nullable=False
    )
    ticket_description: Mapped[Optional[str]] = mapped_column(
        Text, default=None, nullable=True
    )

    sales_start_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )
    sales_end_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )
    complement: Mapped[Optional[str]] = mapped_column(
        String(100), default=None, nullable=True
    )

    poster_url: Mapped[Optional[str]] = mapped_column(
        String(500), default=None, nullable=True
    )
    banner_url: Mapped[Optional[str]] = mapped_column(
        String(500), default=None, nullable=True
    )
    custom_image_url: Mapped[Optional[str]] = mapped_column(
        String(500), default=None, nullable=True
    )
    maps_url: Mapped[Optional[str]] = mapped_column(
        String(500), default=None, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), init=False, default_factory=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        default_factory=datetime.now,
        onupdate=datetime.now,
    )

    organizer: Mapped[Optional['User']] = relationship(init=False)
    tickets: Mapped[list['Ticket']] = relationship(
        'Ticket',
        init=False,
        back_populates='event',
        cascade='all, delete-orphan'
    )

    payout: Mapped[Optional['EventPayout']] = relationship(
        'EventPayout', init=False,
        back_populates='event',
        uselist=False
    )

    @property
    def ticket_info(self):
        return {
            "title": self.ticket_title,
            "description": self.ticket_description,
            "available_tickets": self.available_tickets,
            "ticket_price": self.ticket_price,
            "service_fee": self.service_fee,
        }

    @property
    def location(self):
        return {
            "name": self.location_name,
            "cep": self.cep,
            "address": self.address,
            "number": self.number,
            "neighborhood": self.neighborhood,
            "city": self.city,
            "state": self.state,
            "complement": self.complement,
            "maps_url": self.maps_url,
        }

    @property
    def media(self):
        return {
            "poster_url": self.poster_url,
            "banner_url": self.banner_url,
            "custom_image_url": self.custom_image_url,
        }
