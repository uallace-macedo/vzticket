from decimal import Decimal
from http import HTTPStatus

from vzticket.modules.wallet_claim_tokens.model import ClaimTokenStatus

V1_WALLET_CLAIMS_URL = '/api/v1/wallet/claims'


async def test_create_claim_token_unauthorized(client):
    payload = {'amount': 50.00}
    response = await client.post(V1_WALLET_CLAIMS_URL, json=payload)

    assert response.status_code == HTTPStatus.UNAUTHORIZED


async def test_create_claim_token_success(auth_client):
    payload = {'amount': 50.00}
    response = await auth_client.post(V1_WALLET_CLAIMS_URL, json=payload)

    assert response.status_code == HTTPStatus.CREATED
    json_data = response.json()
    assert 'token' in json_data
    assert Decimal(json_data['amount']) == Decimal('50.00')
    assert json_data['status'] == ClaimTokenStatus.PENDING


async def test_claim_token_success(auth_client):
    create_res = await auth_client.post(
        V1_WALLET_CLAIMS_URL, json={'amount': 100.00}
    )
    token_str = create_res.json()['token']

    claim_payload = {'token': token_str}
    response = await auth_client.post(
        f'{V1_WALLET_CLAIMS_URL}/claim', json=claim_payload
    )

    assert response.status_code == HTTPStatus.OK
    json_data = response.json()
    assert json_data['status'] == ClaimTokenStatus.CLAIMED


async def test_claim_token_not_found(auth_client):
    claim_payload = {'token': '00000000-0000-0000-0000-000000000000'}
    response = await auth_client.post(
        f'{V1_WALLET_CLAIMS_URL}/claim', json=claim_payload
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_get_pending_claims_success(auth_client):
    await auth_client.post(V1_WALLET_CLAIMS_URL, json={'amount': 25.00})

    response = await auth_client.get(f'{V1_WALLET_CLAIMS_URL}/pending')

    assert response.status_code == HTTPStatus.OK
    json_data = response.json()
    assert len(json_data) == 1
    assert json_data[0]['status'] == ClaimTokenStatus.PENDING
