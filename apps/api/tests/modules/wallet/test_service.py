from decimal import Decimal

from vzticket.modules.wallet.model import TransactionType, WalletTransaction
from vzticket.modules.wallet.schemas import WalletTransactionSearch


async def test_wallet_service_get_wallet_empty(wallet_service, user):
    search_params = WalletTransactionSearch(page=1, per_page=10)

    result = await wallet_service.get_wallet(user, search_params)

    assert result.balance == user.balance
    assert result.transactions.total == 0
    assert result.transactions.items == []
    assert result.transactions.page == 1
    assert result.transactions.pages == 1


async def test_wallet_service_get_wallet_with_transactions(
    wallet_service, user, session
):
    tx1 = WalletTransaction(
        user_id=user.id,
        type=TransactionType.DEPOSIT,
        amount=Decimal('100.00'),
        description='Depósito via PIX',
    )
    tx2 = WalletTransaction(
        user_id=user.id,
        type=TransactionType.TICKET_PURCHASE,
        amount=Decimal('50.00'),
        description='Compra de Ingresso',
    )
    session.add_all([tx1, tx2])
    await session.commit()

    search_params = WalletTransactionSearch(page=1, per_page=10)

    result = await wallet_service.get_wallet(user, search_params)

    expected_count = 2
    assert result.balance == user.balance
    assert result.transactions.total == expected_count
    assert len(result.transactions.items) == expected_count
    assert result.transactions.items[0].description == 'Compra de Ingresso'


async def test_wallet_service_get_wallet_filter_by_type(
    wallet_service, user, session
):
    tx1 = WalletTransaction(
        user_id=user.id,
        type=TransactionType.DEPOSIT,
        amount=Decimal('100.00'),
        description='Depósito via PIX',
    )
    tx2 = WalletTransaction(
        user_id=user.id,
        type=TransactionType.TICKET_PURCHASE,
        amount=Decimal('50.00'),
        description='Compra de Ingresso',
    )
    session.add_all([tx1, tx2])
    await session.commit()

    search_params = WalletTransactionSearch(
        type=TransactionType.DEPOSIT,
        page=1,
        per_page=10,
    )

    result = await wallet_service.get_wallet(user, search_params)

    assert result.transactions.total == 1
    assert len(result.transactions.items) == 1
    assert result.transactions.items[0].type == TransactionType.DEPOSIT
