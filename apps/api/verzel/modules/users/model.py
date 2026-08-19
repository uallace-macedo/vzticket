import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from verzel.core.database import table_registry

if TYPE_CHECKING:
    from verzel.modules.events.model import Event
    from verzel.modules.tickets.model import Ticket


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
