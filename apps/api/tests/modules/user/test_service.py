from uuid import uuid4

import pytest

from verzel.modules.users.exceptions import UserAlreadyExistsError, UserNotFoundError
from verzel.modules.users.model import UserRole
from verzel.modules.users.schemas import UserCreate
from verzel.modules.users.service import UserService


async def test_user_service_create_success(session):
    service = UserService(session)
    data = UserCreate(
        name="Novo Usuario",
        email="new@example.com",
        password="password123",
        role=UserRole.CLIENT
    )

    user = await service.create(data)

    assert user.id is not None
    assert user.email == "new@example.com"


async def test_user_service_create_duplicate_email_raises_error(session, user):
    service = UserService(session)
    data = UserCreate(
        name="Outro Nome",
        email=user.email,
        password="password123",
        role=UserRole.CLIENT
    )

    with pytest.raises(UserAlreadyExistsError):
        await service.create(data)


async def test_user_service_get_by_id_not_found_raises_error(session):
    service = UserService(session)

    with pytest.raises(UserNotFoundError):
        await service.get_user_by_id(uuid4())


async def test_user_service_delete_success(session, user):
    service = UserService(session)

    await service.delete(user.id)
    deleted_user = await service.get_user_by_email(user.email)

    assert deleted_user is None
