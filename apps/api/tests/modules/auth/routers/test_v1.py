"""Integration tests for the auth HTTP routes."""

from http import HTTPStatus

from httpx import AsyncClient

from vzticket.core.config import settings

ACCESS_COOKIE = settings.access_token_cookie_name
REFRESH_COOKIE = settings.refresh_token_cookie_name


async def test_register_success(client: AsyncClient, user_payload: dict[str, str]):
    response = await client.post('/api/v1/auth/register', json=user_payload)

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data['email'] == user_payload['email']
    assert data['name'] == user_payload['name']
    assert data['role'] == 'CLIENT'
    assert 'password_hash' not in data


async def test_register_duplicate_email_fails(
    client: AsyncClient, registered_user, user_payload: dict[str, str]
):
    response = await client.post('/api/v1/auth/register', json=user_payload)

    assert response.status_code == HTTPStatus.CONFLICT
    data = response.json()
    assert data['code'] == 'EMAIL_ALREADY_REGISTERED'


async def test_login_success_sets_cookies(client: AsyncClient, registered_user):
    response = await client.post(
        '/api/v1/auth/login',
        data={'username': 'john@example.com', 'password': 'supersecret'},
    )

    assert response.status_code == HTTPStatus.OK
    assert ACCESS_COOKIE in response.cookies
    assert REFRESH_COOKIE in response.cookies
    data = response.json()
    assert data['email'] == 'john@example.com'


async def test_login_invalid_credentials_fails(client: AsyncClient, registered_user):
    response = await client.post(
        '/api/v1/auth/login',
        data={'username': 'john@example.com', 'password': 'wrong-password'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    data = response.json()
    assert data['code'] == 'INVALID_CREDENTIALS'


async def test_refresh_token_success(client: AsyncClient, registered_user):
    login = await client.post(
        '/api/v1/auth/login',
        data={'username': 'john@example.com', 'password': 'supersecret'},
    )
    refresh_cookie = login.cookies.get(REFRESH_COOKIE)
    assert refresh_cookie is not None

    response = await client.post(
        '/api/v1/auth/refresh', cookies={REFRESH_COOKIE: refresh_cookie}
    )

    assert response.status_code == HTTPStatus.OK
    assert ACCESS_COOKIE in response.cookies
    assert REFRESH_COOKIE in response.cookies
    assert response.json()['message'] == 'Tokens atualizados com sucesso.'


async def test_logout_clears_cookies(client: AsyncClient, authenticated_client):
    response = await client.post('/api/v1/auth/logout')

    assert response.status_code == HTTPStatus.OK
    assert response.json()['message'] == 'Logout realizado com sucesso.'
    assert ACCESS_COOKIE not in response.cookies
    assert REFRESH_COOKIE not in response.cookies


async def test_me_authenticated_user(client: AsyncClient, authenticated_client):
    response = await client.get('/api/v1/auth/me')

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['email'] == 'john@example.com'
    assert data['name'] == 'John Doe'


async def test_me_unauthenticated_fails(client: AsyncClient):
    response = await client.get('/api/v1/auth/me')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    data = response.json()
    assert data['code'] == 'UNAUTHORIZED'