from http import HTTPStatus

V1_WALLET_URL = '/api/v1/wallet'


async def test_get_wallet_unauthorized(client):
    response = await client.get(V1_WALLET_URL)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


async def test_get_wallet_success(auth_client):
    response = await auth_client.get(V1_WALLET_URL)

    assert response.status_code == HTTPStatus.OK
    json_data = response.json()
    assert 'balance' in json_data
    assert 'transactions' in json_data
    assert json_data['transactions']['page'] == 1
