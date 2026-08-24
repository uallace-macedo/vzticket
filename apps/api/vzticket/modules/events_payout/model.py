import uuid
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Numeric
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from vzticket.core.database import table_registry

if TYPE_CHECKING:
    from vzticket.modules.events.model import Event
    from vzticket.modules.users.model import User


class PayoutStatus(str, Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    PAID = 'paid'
    FAILED = 'failed'


@table_registry.mapped_as_dataclass
class EventPayout:
    __tablename__ = 'tb_event_payouts'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False,
        primary_key=True,
        default_factory=uuid.uuid4
    )

    event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('tb_events.id'),
        unique=True,
        nullable=False
    )

    organizer_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('tb_users.id'),
        nullable=False
    )

    gross_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    platform_fee_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    net_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    scheduled_for: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    status: Mapped[PayoutStatus] = mapped_column(
        SQLEnum(PayoutStatus, native_enum=False),
        default=PayoutStatus.PENDING,
        nullable=False
    )

    paid_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=None,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        default_factory=lambda: datetime.now(timezone.utc)
    )

    event: Mapped['Event'] = relationship(
        init=False,
        back_populates='payout'
    )

    organizer: Mapped['User'] = relationship(
        init=False,
        back_populates='payouts'
    )
