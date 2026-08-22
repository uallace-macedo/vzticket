import enum
import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from vzticket.core.database import table_registry

if TYPE_CHECKING:
    from vzticket.modules.users.model import User


class ClaimTokenStatus(str, enum.Enum):
    PENDING = 'PENDING'
    CLAIMED = 'CLAIMED'
    EXPIRED = 'EXPIRED'


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
    status: Mapped[ClaimTokenStatus] = mapped_column(
        Enum(ClaimTokenStatus),
        init=False,
        default=ClaimTokenStatus.PENDING, nullable=False
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
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

    user: Mapped[Optional['User']] = relationship(init=False)
