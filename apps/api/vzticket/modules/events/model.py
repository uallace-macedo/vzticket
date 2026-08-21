import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from vzticket.core.database import table_registry
from typing import Optional

if TYPE_CHECKING:
    from vzticket.modules.tickets.model import Ticket
    from vzticket.modules.users.model import User


@table_registry.mapped_as_dataclass
class Event:
    __tablename__ = 'tb_events'
    __table_args__ = (
        Index('idx_events_state_city', 'state', 'city_slug'),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        init=False,
        primary_key=True,
        default_factory=uuid.uuid4
    )

    organizer_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('tb_users.id'),
        nullable=False
    )

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    available_tickets: Mapped[int] = mapped_column(nullable=False)
    ticket_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )
    event_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    location_name: Mapped[str] = mapped_column(String(150), nullable=False)
    cep: Mapped[str] = mapped_column(String(9), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    number: Mapped[str] = mapped_column(String(20), nullable=False)
    neighborhood: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    city_slug: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    state: Mapped[str] = mapped_column(String(2), nullable=False)

    poster_url: Mapped[Optional[str]] = mapped_column(String(500), default=None)
    banner_url: Mapped[Optional[str]] = mapped_column(String(500), default=None)
    complement: Mapped[Optional[str]] = mapped_column(String(100), default=None)
    custom_image_url: Mapped[Optional[str]] = mapped_column(String(500), default=None)
    maps_url: Mapped[Optional[str]] = mapped_column(String(500), default=None)

    organizer: Mapped['User'] = relationship(
        init=False,
        back_populates='events'
    )

    tickets: Mapped[List['Ticket']] = relationship(
        init=False,
        back_populates='event',
        cascade='all, delete-orphan'
    )
