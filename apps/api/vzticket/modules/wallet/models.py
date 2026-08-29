import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from vzticket.core.database import Base
from vzticket.modules.auth.models import User
from vzticket.modules.events.models import Event


class TransactionType(str, enum.Enum):
    DEPOSIT = 'DEPOSIT'
    TICKET_PURCHASE = 'TICKET_PURCHASE'
    TICKET_REFUND = 'TICKET_REFUND'
    EVENT_CREATION_FEE = 'EVENT_CREATION_FEE'
    EVENT_PAYOUT = 'EVENT_PAYOUT'


class ClaimTokenType(str, enum.Enum):
    DEPOSIT = 'DEPOSIT'
    TICKET_PURCHASE = 'TICKET_PURCHASE'
    EVENT_FEE = 'EVENT_FEE'


class ClaimTokenStatus(str, enum.Enum):
    PENDING = 'PENDING'
    CLAIMED = 'CLAIMED'
    EXPIRED = 'EXPIRED'


class PayoutStatus(str, enum.Enum):
    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    PAID = 'PAID'
    FAILED = 'FAILED'


class WalletTransaction(Base):
    __tablename__ = 'wallet_transactions'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.id')
    )
    event_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey('events.id'), nullable=True
    )
    ticket_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey('tickets.id'), nullable=True
    )
    type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType, name='transaction_type')
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    description: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped[User] = relationship()


class WalletClaimToken(Base):
    __tablename__ = 'wallet_claim_tokens'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    token: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    type: Mapped[ClaimTokenType] = mapped_column(
        Enum(ClaimTokenType, name='claim_token_type')
    )
    target_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.id'), nullable=True
    )
    status: Mapped[ClaimTokenStatus] = mapped_column(
        Enum(ClaimTokenStatus, name='claim_token_status'),
        default=ClaimTokenStatus.PENDING,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    claimed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class EventPayout(Base):
    __tablename__ = 'event_payouts'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('events.id'), unique=True
    )
    organizer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.id')
    )
    gross_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    platform_fee_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    net_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    status: Mapped[PayoutStatus] = mapped_column(
        Enum(PayoutStatus, name='payout_status'), default=PayoutStatus.PENDING
    )
    scheduled_for: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    event: Mapped[Event] = relationship()
    organizer: Mapped[User] = relationship()
