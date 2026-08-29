"""Pydantic schemas for the auth module."""

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from vzticket.modules.auth.models import UserRole


class UserRegister(BaseModel):
    """Payload for registering a new user."""

    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: UserRole


class UserLogin(BaseModel):
    """Payload for authenticating a user."""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Public representation of a user."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    email: EmailStr
    role: UserRole
    balance: Decimal
    created_at: datetime


class MessageResponse(BaseModel):
    """Generic message response."""

    message: str
