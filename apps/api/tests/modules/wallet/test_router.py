from http import HTTPStatus

from vzticket.modules.wallet.model import TransactionType

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


async def test_deposit_route_success(auth_client):
    amount = '100.00'
    payload = {
        'amount': 100.00
    }

    response = await auth_client.post(V1_WALLET_URL, json=payload)

    assert response.status_code == HTTPStatus.CREATED
    json_data = response.json()
    assert json_data['message'] == 'Depósito efetuado com sucesso'
    assert json_data['new_balance'] == amount
    assert json_data['transaction']['type'] == TransactionType.DEPOSIT.value


async def test_deposit_route_invalid_amount(auth_client):
    payload = {
        'amount': -10.00
    }

    response = await auth_client.post(V1_WALLET_URL, json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
