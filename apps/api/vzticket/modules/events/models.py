import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from vzticket.core.database import Base
from vzticket.modules.auth.models import User


class EventStatus(str, enum.Enum):
    PENDING_FEE = 'PENDING_FEE'
    ACTIVE = 'ACTIVE'
    CANCELLED = 'CANCELLED'
    FINISHED = 'FINISHED'


class Event(Base):
    __tablename__ = 'events'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    organizer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.id')
    )
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[EventStatus] = mapped_column(
        Enum(EventStatus, name='event_status'), default=EventStatus.PENDING_FEE
    )
    available_tickets: Mapped[int] = mapped_column(Integer)
    ticket_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    service_fee: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    ticket_title: Mapped[str] = mapped_column(String(100), default='Pista')
    ticket_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    event_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), index=True
    )
    sales_start_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    sales_end_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    location_name: Mapped[str] = mapped_column(String(150))
    cep: Mapped[str] = mapped_column(String(8))
    address: Mapped[str] = mapped_column(String(255))
    number: Mapped[str] = mapped_column(String(20))
    neighborhood: Mapped[str] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(100))
    city_slug: Mapped[str] = mapped_column(String(100), index=True)
    state: Mapped[str] = mapped_column(String(2))
    complement: Mapped[str | None] = mapped_column(String(100), nullable=True)
    poster_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    banner_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    custom_image_url: Mapped[str | None] = mapped_column(
        String(500), nullable=True
    )
    maps_url: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    organizer: Mapped[User] = relationship()

    __table_args__ = (
        CheckConstraint(
            'available_tickets >= 0', name='ck_events_available_tickets_positive'
        ),
        CheckConstraint('ticket_price >= 0.00', name='ck_events_ticket_price_positive'),
        CheckConstraint('service_fee >= 0.00', name='ck_events_service_fee_positive'),
    )
