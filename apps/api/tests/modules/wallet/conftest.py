import pytest

from vzticket.modules.wallet.repository import WalletRepository


@pytest.fixture
def wallet_repository(session):
    return WalletRepository(session)
