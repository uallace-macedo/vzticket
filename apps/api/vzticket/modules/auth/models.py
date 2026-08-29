import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, Enum, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from vzticket.core.database import Base


class UserRole(str, enum.Enum):
    CLIENT = 'CLIENT'
    ORGANIZER = 'ORGANIZER'
    GATEKEEPER = 'GATEKEEPER'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name='user_role'), default=UserRole.CLIENT
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), default=Decimal('0.00'), server_default='0.00'
    )
    pending_balance: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), default=Decimal('0.00'), server_default='0.00'
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        CheckConstraint('balance >= 0.00', name='ck_users_balance_positive'),
        CheckConstraint(
            'pending_balance >= 0.00', name='ck_users_pending_balance_positive'
        ),
    )
