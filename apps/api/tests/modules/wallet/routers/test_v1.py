"""Integration tests for the wallet HTTP routes."""

from http import HTTPStatus

from httpx import AsyncClient


async def test_create_deposit_claim_success(
    client: AsyncClient, authenticated_wallet_client
):
    response = await client.post(
        '/api/v1/wallet/deposit', json={'amount': '50.00'}
    )

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data['amount'] == '50.00'
    assert data['type'] == 'DEPOSIT'
    assert data['status'] == 'PENDING'
    assert data['token']


async def test_claim_deposit_success(
    client: AsyncClient, authenticated_wallet_client, pending_claim_token: str
):
    response = await client.post(f'/api/v1/wallet/claim/{pending_claim_token}')

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['type'] == 'DEPOSIT'
    assert data['amount'] == '50.00'


async def test_claim_expired_token_fails(
    client: AsyncClient, authenticated_wallet_client, expired_claim_token: str
):
    response = await client.post(f'/api/v1/wallet/claim/{expired_claim_token}')

    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.json()
    assert data['code'] == 'EXPIRED_CLAIM_TOKEN'


async def test_claim_already_used_token_fails(
    client: AsyncClient, authenticated_wallet_client, claimed_claim_token: str
):
    response = await client.post(f'/api/v1/wallet/claim/{claimed_claim_token}')

    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.json()
    assert data['code'] == 'CLAIM_TOKEN_ALREADY_USED'


async def test_get_balance(client: AsyncClient, authenticated_wallet_client):
    response = await client.get('/api/v1/wallet/me/balance')

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['balance'] == '100.00'
    assert data['pending_balance'] == '0.00'


async def test_get_transactions_audit_log(
    client: AsyncClient, authenticated_wallet_client, pending_claim_token: str
):
    await client.post(f'/api/v1/wallet/claim/{pending_claim_token}')

    response = await client.get('/api/v1/wallet/transactions')

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data) == 1
    assert data[0]['type'] == 'DEPOSIT'
    assert data[0]['amount'] == '50.00'