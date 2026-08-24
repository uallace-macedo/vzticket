
import pytest
from fastapi.security import OAuth2PasswordRequestForm

from vzticket.modules.auth.exceptions import InvalidCredentialsError
from vzticket.modules.auth.service import AuthService


async def test_auth_service_login_success(session, user):
    auth_service = AuthService(session)
    form_data = OAuth2PasswordRequestForm(
        username=user.email,
        password="password123",
        scope="",
        grant_type="password"
    )

    token, db_user = await auth_service.login(form_data)

    assert isinstance(token, str)
    assert db_user.id == user.id


async def test_auth_service_login_invalid_password_raises_error(session, user):
    auth_service = AuthService(session)
    form_data = OAuth2PasswordRequestForm(
        username=user.email,
        password="wrongpassword",
        scope="",
        grant_type="password"
    )

    with pytest.raises(InvalidCredentialsError):
        await auth_service.login(form_data)
