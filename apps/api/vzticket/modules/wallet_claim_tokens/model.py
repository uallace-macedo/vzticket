import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from vzticket.core.database import table_registry

if TYPE_CHECKING:
    from vzticket.modules.users.model import User


class ClaimTokenStatus(str, Enum):
    PENDING = 'pending'
    CLAIMED = 'claimed'
    EXPIRED = 'expired'


class ClaimType(str, Enum):
    DEPOSIT = 'deposit'
    TICKET_PURCHASE = 'ticket_purchase'
    EVENT_FEE = 'event_fee'


@table_registry.mapped_as_dataclass
class WalletClaimToken:
    __tablename__ = 'tb_wallet_claim_tokens'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False,
        primary_key=True,
        default_factory=uuid.uuid4
    )

    token: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        index=True,
        nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    type: Mapped[ClaimType] = mapped_column(
        SQLEnum(ClaimType, native_enum=False),
        default=ClaimType.DEPOSIT,
        nullable=False
    )

    target_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        default=None,
        nullable=True
    )

    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey('tb_users.id'),
        default=None,
        nullable=True,
        index=True
    )

    claimed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=None,
        nullable=True
    )

    status: Mapped[ClaimTokenStatus] = mapped_column(
        SQLEnum(ClaimTokenStatus, native_enum=False),
        init=False,
        default=ClaimTokenStatus.PENDING,
        nullable=False
    )

    user: Mapped[Optional['User']] = relationship(init=False)
