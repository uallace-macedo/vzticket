import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from vzticket.core.database import table_registry

if TYPE_CHECKING:
    from vzticket.modules.tickets.model import Ticket
    from vzticket.modules.users.model import User


@table_registry.mapped_as_dataclass
class Event:
    __tablename__ = 'tb_events'

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

    location: Mapped[str] = mapped_column(String(255), nullable=False)
    event_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    location_url: Mapped[str | None] = mapped_column(default=None, nullable=True)

    poster_url: Mapped[str | None] = mapped_column(default=None)
    banner_url: Mapped[str | None] = mapped_column(default=None)

    organizer: Mapped['User'] = relationship(
        init=False,
        back_populates='events'
    )

    tickets: Mapped[List['Ticket']] = relationship(
        init=False,
        back_populates='event',
        cascade='all, delete-orphan'
    )
