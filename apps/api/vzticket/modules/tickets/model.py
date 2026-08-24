import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from vzticket.core.database import table_registry

if TYPE_CHECKING:
    from vzticket.modules.events.model import Event
    from vzticket.modules.users.model import User


class TicketStatus(str, Enum):
    VALID = 'valid'
    USED = 'used'
    CANCELLED = 'canceled'


@table_registry.mapped_as_dataclass
class Ticket:
    __tablename__ = 'tb_tickets'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False,
        primary_key=True,
        default_factory=uuid.uuid4
    )

    event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('tb_events.id'),
        nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('tb_users.id'),
        nullable=False
    )

    qr_code_hash: Mapped[str] = mapped_column(nullable=False)

    share_token: Mapped[uuid.UUID] = mapped_column(
        default_factory=uuid.uuid4,
        unique=True
    )

    status: Mapped[TicketStatus] = mapped_column(
        SQLEnum(TicketStatus, native_enum=False),
        default=TicketStatus.VALID
    )

    purchased_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=lambda: datetime.now(timezone.utc)
    )

    validated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=None
    )

    user: Mapped['User'] = relationship(
        init=False,
        back_populates='tickets'
    )

    event: Mapped['Event'] = relationship(
        init=False,
        back_populates='tickets'
    )
