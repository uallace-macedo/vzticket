import pytest

from vzticket.modules.wallet.repository import WalletRepository
from vzticket.modules.wallet.service import WalletService


@pytest.fixture
def wallet_service(session):
    return WalletService(session)


@pytest.fixture
def wallet_repository(session):
    return WalletRepository(session)
