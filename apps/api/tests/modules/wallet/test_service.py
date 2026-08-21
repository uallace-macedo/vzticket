from decimal import Decimal

import pytest

from vzticket.modules.wallet.model import TransactionType
from vzticket.modules.wallet.schemas import WalletTransactionSearch
from vzticket.modules.wallet.service import WalletService


@pytest.fixture
def wallet_service(session):
    return WalletService(session)


async def test_wallet_service_deposit_success(wallet_service, user):
    initial_balance = user.balance
    deposit_amount = Decimal('150.00')

    response = await wallet_service.deposit(user, deposit_amount)

    assert response.message == 'Depósito efetuado com sucesso'
    assert response.new_balance == initial_balance + deposit_amount
    assert response.transaction.amount == deposit_amount
    assert response.transaction.type == TransactionType.DEPOSIT


async def test_wallet_service_get_wallet_success(wallet_service, user):
    await wallet_service.deposit(user, Decimal('50.00'))

    params = WalletTransactionSearch(page=1, per_page=10)
    wallet_data = await wallet_service.get_wallet(user, params)

    assert wallet_data.balance == Decimal('50.00')
    assert wallet_data.transactions.total == 1
    assert wallet_data.transactions.items[0].amount == Decimal('50.00')
    assert wallet_data.transactions.items[0].type == TransactionType.DEPOSIT
