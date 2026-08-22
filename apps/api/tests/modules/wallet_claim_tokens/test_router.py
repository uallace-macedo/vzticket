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


async def test_process_payment_via_qr_success(auth_client):
    create_res = await auth_client.post(
        V1_WALLET_CLAIMS_URL, json={'amount': 100.00}
    )
    token_str = create_res.json()['token']

    response = await auth_client.get(
        f'{V1_WALLET_CLAIMS_URL}/pay', params={'token': token_str}
    )

    assert response.status_code == HTTPStatus.OK
    assert "text/html" in response.headers["content-type"]

    html_text = response.text
    assert "<!DOCTYPE html>" in html_text
    assert "Depósito Confirmado" in html_text
    assert "R$ 100,00" in html_text


async def test_process_payment_via_qr_not_found(auth_client):
    fake_token = '00000000-0000-0000-0000-000000000000'
    response = await auth_client.get(
        f'{V1_WALLET_CLAIMS_URL}/pay', params={'token': fake_token}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_get_pending_claims_success(auth_client):
    await auth_client.post(V1_WALLET_CLAIMS_URL, json={'amount': 25.00})

    response = await auth_client.get(f'{V1_WALLET_CLAIMS_URL}/pending')

    assert response.status_code == HTTPStatus.OK
    json_data = response.json()
    assert len(json_data) == 1
    assert json_data[0]['status'] == ClaimTokenStatus.PENDING
