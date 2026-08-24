import uuid
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from vzticket.core.database import table_registry

if TYPE_CHECKING:
    from vzticket.modules.events.model import Event
    from vzticket.modules.tickets.model import Ticket
    from vzticket.modules.users.model import User


class TransactionType(str, Enum):
    DEPOSIT = 'deposit'
    TICKET_PURCHASE = 'ticket_purchase'
    TICKET_REFUND = 'ticket_refund'
    EVENT_CREATION_FEE = 'event_creation_fee'
    EVENT_PAYOUT = 'event_payout'


@table_registry.mapped_as_dataclass
class WalletTransaction:
    __tablename__ = 'tb_wallet_transactions'
    __table_args__ = (
        Index('idx_wallet_tx_user_type', 'user_id', 'type'),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        init=False,
        primary_key=True,
        default_factory=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('tb_users.id'),
        nullable=False
    )

    type: Mapped[TransactionType] = mapped_column(
        SQLEnum(TransactionType, native_enum=False),
        nullable=False,
        index=True
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    event_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey('tb_events.id'),
        default=None
    )

    ticket_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey('tb_tickets.id'),
        default=None
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        default_factory=lambda: datetime.now(timezone.utc)
    )

    user: Mapped['User'] = relationship(
        init=False,
        back_populates='wallet_transactions'
    )

    event: Mapped[Optional['Event']] = relationship(
        init=False
    )

    ticket: Mapped[Optional['Ticket']] = relationship(
        init=False
    )
