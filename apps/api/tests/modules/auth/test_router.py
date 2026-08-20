from http import HTTPStatus

from vzticket.modules.users.model import UserRole

V1_BASE_URL = '/api/v1/auth'


async def test_register_route_success(client):
    payload = {
        "name": "User Router Test",
        "email": "route_user@example.com",
        "password": "password123",
        "role": UserRole.CLIENT.value
    }

    response = await client.post(f'{V1_BASE_URL}/register', json=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["email"] == payload["email"]


async def test_register_route_duplicate_email(client, user):
    payload = {
        "name": "User Duplicate Test",
        "email": user.email,
        "password": "password123",
        "role": UserRole.CLIENT.value
    }

    response = await client.post(f'{V1_BASE_URL}/register', json=payload)

    assert response.status_code == HTTPStatus.CONFLICT


async def test_login_route_success(client, user):
    payload = {
        "username": user.email,
        "password": "password123"
    }

    response = await client.post(f'{V1_BASE_URL}/login', data=payload)

    assert response.status_code == HTTPStatus.OK
    assert response.json()["email"] == user.email


async def test_login_route_invalid_credentials(client, user):
    payload = {
        "username": user.email,
        "password": "wrongpassword"
    }

    response = await client.post(f'{V1_BASE_URL}/login', data=payload)

    assert response.status_code == HTTPStatus.UNAUTHORIZED


async def test_logout_route_success(auth_client):
    response = await auth_client.post(f'{V1_BASE_URL}/logout')

    assert response.status_code == HTTPStatus.NO_CONTENT
