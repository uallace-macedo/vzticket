import uuid
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DECIMAL, DateTime, Numeric, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from vzticket.core.database import table_registry

if TYPE_CHECKING:
    from vzticket.modules.events.model import Event
    from vzticket.modules.tickets.model import Ticket
    from vzticket.modules.wallet.model import WalletTransaction
    from vzticket.modules.wallet_claim_tokens.model import WalletClaimToken


class UserRole(str, Enum):
    ORGANIZER = 'organizer'
    CLIENT = 'client'
    GATEKEEPER = 'gatekeeper'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'tb_users'

    id: Mapped[uuid.UUID] = mapped_column(
        init=False,
        primary_key=True,
        default_factory=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, native_enum=False),
        nullable=False
    )

    balance: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2),
        init=False,
        default=Decimal('0.00'),
        server_default='0.00'
    )
    pending_balance: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=Decimal('0.00'),
        server_default='0.00'
    )

    image_url: Mapped[Optional[str]] = mapped_column(
        String(255),
        default=None,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        default_factory=lambda: datetime.now(timezone.utc)
    )

    events: Mapped[List['Event']] = relationship(
        init=False,
        back_populates='organizer',
        cascade='all, delete-orphan'
    )

    tickets: Mapped[List['Ticket']] = relationship(
        init=False,
        back_populates='user',
        cascade='all, delete-orphan'
    )

    wallet_transactions: Mapped[List['WalletTransaction']] = relationship(
        init=False,
        back_populates='user',
        cascade='all, delete-orphan'
    )

    wallet_claims: Mapped[List['WalletClaimToken']] = relationship(
        init=False,
        back_populates='user'
    )
