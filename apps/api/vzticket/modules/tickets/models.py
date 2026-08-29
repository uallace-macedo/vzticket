import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from vzticket.core.database import Base
from vzticket.modules.auth.models import User
from vzticket.modules.events.models import Event


class TicketStatus(str, enum.Enum):
    VALID = 'VALID'
    USED = 'USED'
    CANCELLED = 'CANCELLED'


class Ticket(Base):
    __tablename__ = 'tickets'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('events.id')
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.id')
    )
    status: Mapped[TicketStatus] = mapped_column(
        Enum(TicketStatus, name='ticket_status'), default=TicketStatus.VALID
    )
    qr_code_hash: Mapped[str] = mapped_column(String(255))
    purchased_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    validated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    event: Mapped[Event] = relationship()
    user: Mapped[User] = relationship()

    __table_args__ = (
        Index('ix_tickets_user_status', 'user_id', 'status'),
        Index('ix_tickets_event_status', 'event_id', 'status'),
    )
