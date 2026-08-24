from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from vzticket.modules.users.model import UserRole
from enum import Enum


class TokenType(str, Enum):
    ACCESS = 'access'
    REFRESH = 'refresh'


class TokenPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sub: UUID
    type: TokenType
    email: EmailStr
    role: UserRole
    exp: Optional[int] = Field(default=None)
