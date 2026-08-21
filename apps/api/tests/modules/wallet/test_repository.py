from decimal import Decimal

import pytest

from vzticket.modules.wallet.repository import WalletRepository
from vzticket.modules.wallet.schemas import WalletTransactionSearch
from vzticket.modules.wallet.model import (
    TransactionType,
    WalletTransaction,
)


@pytest.fixture
def wallet_repository(session):
    return WalletRepository(session)


async def test_wallet_repository_create_transaction_success(
    wallet_repository, user
):
    transaction = WalletTransaction(
        user_id=user.id,
        type=TransactionType.DEPOSIT,
        amount=Decimal('100.00'),
        description='Depósito Inicial',
    )

    saved_tx = await wallet_repository.create(transaction)

    assert saved_tx.id is not None
    assert saved_tx.user_id == user.id
    assert saved_tx.amount == Decimal('100.00')
    assert saved_tx.type == TransactionType.DEPOSIT


async def test_wallet_repository_get_by_user_id_paginated(
    wallet_repository, user
):
    total_transactions = 3
    expected_page_items = 2
    expected_total_pages = 2

    for i in range(total_transactions):
        tx = WalletTransaction(
            user_id=user.id,
            type=TransactionType.DEPOSIT,
            amount=Decimal(f'{10 * (i + 1)}.00'),
            description=f'Depósito {i + 1}',
        )
        await wallet_repository.create(tx)

    search_params = WalletTransactionSearch(page=1, per_page=2)
    transactions, total, pages = (
        await wallet_repository.get_by_user_id_paginated(user.id, search_params)
    )

    assert len(transactions) == expected_page_items
    assert total == total_transactions
    assert pages == expected_total_pages


async def test_wallet_repository_filter_by_type(wallet_repository, user):
    tx_deposit = WalletTransaction(
        user_id=user.id,
        type=TransactionType.DEPOSIT,
        amount=Decimal('50.00'),
        description='Depósito PIX',
    )
    tx_purchase = WalletTransaction(
        user_id=user.id,
        type=TransactionType.TICKET_PURCHASE,
        amount=Decimal('20.00'),
        description='Compra de Ingresso',
    )
    await wallet_repository.create(tx_deposit)
    await wallet_repository.create(tx_purchase)

    search_params = WalletTransactionSearch(
        type=TransactionType.TICKET_PURCHASE, page=1, per_page=10
    )
    transactions, total, pages = (
        await wallet_repository.get_by_user_id_paginated(user.id, search_params)
    )

    assert len(transactions) == 1
    assert total == 1
    assert transactions[0].type == TransactionType.TICKET_PURCHASE
