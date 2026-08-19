from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from verzel.modules.users.model import UserRole


class TokenPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sub: UUID
    email: EmailStr
    role: UserRole
    exp: Optional[int] = Field(default=None)
