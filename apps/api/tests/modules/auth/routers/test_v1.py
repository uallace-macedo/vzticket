"""Integration tests for the auth module."""

import pytest
from httpx import AsyncClient

from vzticket.core.config import settings

REGISTER_URL = '/api/v1/auth/register'
LOGIN_URL = '/api/v1/auth/login'
REFRESH_URL = '/api/v1/auth/refresh'
LOGOUT_URL = '/api/v1/auth/logout'
ME_URL = '/api/v1/auth/me'

ACCESS_COOKIE = settings.access_token_cookie_name
REFRESH_COOKIE = settings.refresh_token_cookie_name

USER_PAYLOAD = {
    'name': 'Test User',
    'username': 'test2@example.com',
    'email': 'test2@example.com',
    'password': 'supersecret123',
    'role': 'CLIENT',
}


async def test_register_success(client: AsyncClient) -> None:
    response = await client.post(REGISTER_URL, json=USER_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    assert data['email'] == USER_PAYLOAD['email']
    assert data['name'] == USER_PAYLOAD['name']
    assert 'password' not in data
    assert 'password_hash' not in data


async def test_register_duplicate_email(client: AsyncClient) -> None:
    await client.post(REGISTER_URL, json=USER_PAYLOAD)
    response = await client.post(REGISTER_URL, json=USER_PAYLOAD)
    assert response.status_code == 409
    data = response.json()
    assert data['code'] == 'EMAIL_ALREADY_REGISTERED'


async def test_register_validation_error(client: AsyncClient) -> None:
    response = await client.post(
        REGISTER_URL, json={'name': '', 'email': 'not-an-email', 'password': 'short'}
    )
    assert response.status_code == 422
    data = response.json()
    assert data['code'] == 'VALIDATION_ERROR'


async def test_login_success_sets_cookies(client: AsyncClient) -> None:
    await client.post(REGISTER_URL, json=USER_PAYLOAD)
    response = await client.post(
        LOGIN_URL,
        data={'username': USER_PAYLOAD['email'], 'password': USER_PAYLOAD['password']},
    )
    assert response.status_code == 200
    assert ACCESS_COOKIE in response.cookies
    assert REFRESH_COOKIE in response.cookies
    data = response.json()
    assert data['email'] == USER_PAYLOAD['email']


async def test_login_invalid_credentials(client: AsyncClient) -> None:
    await client.post(REGISTER_URL, json=USER_PAYLOAD)
    response = await client.post(
        LOGIN_URL,
        data={'username': USER_PAYLOAD['email'], 'password': 'wrongpassword'},
    )
    assert response.status_code == 401
    data = response.json()
    assert data['code'] == 'INVALID_CREDENTIALS'


async def test_login_unknown_email(client: AsyncClient) -> None:
    response = await client.post(
        LOGIN_URL,
        data={'username': 'nobody@example.com', 'password': 'whatever123'},
    )
    assert response.status_code == 401
    data = response.json()
    assert data['code'] == 'INVALID_CREDENTIALS'


async def test_me_with_cookie(client: AsyncClient) -> None:
    await client.post(REGISTER_URL, json=USER_PAYLOAD)
    login = await client.post(
        LOGIN_URL,
        data={'username': USER_PAYLOAD['email'], 'password': USER_PAYLOAD['password']},
    )
    response = await client.get(ME_URL, cookies=login.cookies)
    assert response.status_code == 200
    data = response.json()
    assert data['email'] == USER_PAYLOAD['email']


async def test_me_with_bearer_header(client: AsyncClient) -> None:
    await client.post(REGISTER_URL, json=USER_PAYLOAD)
    login = await client.post(
        LOGIN_URL,
        data={'username': USER_PAYLOAD['email'], 'password': USER_PAYLOAD['password']},
    )
    access_token = login.cookies[ACCESS_COOKIE]
    response = await client.get(
        ME_URL, headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['email'] == USER_PAYLOAD['email']


async def test_me_unauthorized(client: AsyncClient) -> None:
    response = await client.get(ME_URL)
    assert response.status_code == 401
    data = response.json()
    assert data['code'] == 'UNAUTHORIZED'


async def test_me_invalid_token(client: AsyncClient) -> None:
    response = await client.get(
        ME_URL, headers={'Authorization': 'Bearer not-a-valid-token'}
    )
    assert response.status_code == 401
    data = response.json()
    assert data['code'] == 'INVALID_TOKEN'


async def test_refresh_rotates_tokens(client: AsyncClient) -> None:
    await client.post(REGISTER_URL, json=USER_PAYLOAD)
    login = await client.post(
        LOGIN_URL,
        data={'username': USER_PAYLOAD['email'], 'password': USER_PAYLOAD['password']},
    )
    response = await client.post(REFRESH_URL, cookies=login.cookies)
    assert response.status_code == 200
    assert ACCESS_COOKIE in response.cookies
    assert REFRESH_COOKIE in response.cookies
    data = response.json()
    assert data['message'] == 'Tokens atualizados com sucesso.'


async def test_refresh_without_cookie(client: AsyncClient) -> None:
    response = await client.post(REFRESH_URL)
    assert response.status_code == 401
    data = response.json()
    assert data['code'] == 'INVALID_TOKEN'


async def test_refresh_invalid_token(client: AsyncClient) -> None:
    response = await client.post(
        REFRESH_URL, cookies={REFRESH_COOKIE: 'garbage-token'}
    )
    assert response.status_code == 401
    data = response.json()
    assert data['code'] == 'INVALID_TOKEN'


async def test_logout_clears_cookies(client: AsyncClient) -> None:
    await client.post(REGISTER_URL, json=USER_PAYLOAD)
    login = await client.post(
        LOGIN_URL,
        data={'username': USER_PAYLOAD['email'], 'password': USER_PAYLOAD['password']},
    )
    response = await client.post(LOGOUT_URL, cookies=login.cookies)
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Logout realizado com sucesso.'
    assert response.cookies.get(ACCESS_COOKIE) in (None, '')
    assert response.cookies.get(REFRESH_COOKIE) in (None, '')


async def test_logout_unauthorized(client: AsyncClient) -> None:
    response = await client.post(LOGOUT_URL)
    assert response.status_code == 401
    data = response.json()
    assert data['code'] == 'UNAUTHORIZED'
