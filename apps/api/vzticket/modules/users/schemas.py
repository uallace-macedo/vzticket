from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from vzticket.modules.users.model import UserRole


class UserBase(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    role: UserRole
    image_url: Optional[str] = Field(default=None)


class UserCreate(UserBase):
    password: str = Field(min_length=6)


class UserPublic(UserBase):
    id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )
