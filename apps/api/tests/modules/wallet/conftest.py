"""Shared fixtures for the wallet module tests."""

import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from vzticket.core.config import settings
from vzticket.modules.auth.models import User, UserRole
from vzticket.modules.auth.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
)
from vzticket.modules.wallet.models import (
    ClaimTokenStatus,
    ClaimTokenType,
    WalletClaimToken,
    WalletTransaction,
)


@pytest.fixture
def user_factory():
    """Factory that builds a User with an initialized wallet."""

    def _make_user(**overrides: object) -> User:
        defaults: dict[str, object] = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'password_hash': hash_password('supersecret'),
            'role': UserRole.CLIENT,
            'balance': Decimal('100.00'),
            'pending_balance': Decimal('0.00'),
        }
        defaults.update(overrides)
        return User(**defaults)

    return _make_user


@pytest.fixture
async def wallet_user(session, user_factory) -> User:
    """Seed a user with an initialized wallet in the database."""
    user = user_factory()
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest.fixture
async def authenticated_wallet_client(client, wallet_user):
    """AsyncClient authenticated as the wallet user."""
    client.cookies.set(
        settings.access_token_cookie_name,
        create_access_token(str(wallet_user.id)),
    )
    client.cookies.set(
        settings.refresh_token_cookie_name,
        create_refresh_token(str(wallet_user.id)),
    )
    return client


def _claim_token(
    user_id: uuid.UUID,
    *,
    status: ClaimTokenStatus,
    expires_at: datetime,
    amount: Decimal = Decimal('50.00'),
) -> WalletClaimToken:
    return WalletClaimToken(
        token=str(uuid.uuid4()),
        amount=amount,
        type=ClaimTokenType.DEPOSIT,
        user_id=user_id,
        status=status,
        expires_at=expires_at,
    )


@pytest.fixture
async def pending_claim_token(session, wallet_user) -> str:
    """Insert a valid pending deposit claim token and return its string."""
    token = _claim_token(
        wallet_user.id,
        status=ClaimTokenStatus.PENDING,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=15),
    )
    session.add(token)
    await session.commit()
    return token.token


@pytest.fixture
async def expired_claim_token(session, wallet_user) -> str:
    """Insert an expired deposit claim token and return its string."""
    token = _claim_token(
        wallet_user.id,
        status=ClaimTokenStatus.PENDING,
        expires_at=datetime.now(timezone.utc) - timedelta(minutes=1),
    )
    session.add(token)
    await session.commit()
    return token.token


@pytest.fixture
async def claimed_claim_token(session, wallet_user) -> str:
    """Insert a CLAIMED deposit claim token and return its string."""
    token = _claim_token(
        wallet_user.id,
        status=ClaimTokenStatus.CLAIMED,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=15),
    )
    session.add(token)
    await session.commit()
    return token.token


class FakeWalletRepository:
    """In-memory repository used for wallet service unit tests."""

    def __init__(self) -> None:
        self._tokens: dict[str, WalletClaimToken] = {}
        self._users: dict[uuid.UUID, User] = {}
        self._transactions: list[WalletTransaction] = []

    def add_user(self, user: User) -> None:
        self._users[user.id] = user

    async def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        return self._users.get(user_id)

    async def get_user_by_id_for_update(self, user_id: uuid.UUID) -> User | None:
        return self._users.get(user_id)

    async def get_claim_token_for_update(
        self, token: str
    ) -> WalletClaimToken | None:
        return self._tokens.get(token)

    async def create_claim_token(
        self, token: WalletClaimToken
    ) -> WalletClaimToken:
        self._tokens[token.token] = token
        return token

    async def create_transaction(
        self, transaction: WalletTransaction
    ) -> WalletTransaction:
        self._transactions.append(transaction)
        return transaction

    async def get_user_transactions(
        self, user_id: uuid.UUID
    ) -> list[WalletTransaction]:
        return [t for t in self._transactions if t.user_id == user_id]

    async def get_pending_claim_token(
        self, user_id: uuid.UUID
    ) -> WalletClaimToken | None:
        for token in self._tokens.values():
            if (
                token.user_id == user_id
                and token.status == ClaimTokenStatus.PENDING
            ):
                return token
        return None

    async def commit(self) -> None:
        pass


@pytest.fixture
def fake_wallet_repository() -> FakeWalletRepository:
    """Fresh in-memory repository for wallet service unit tests."""
    return FakeWalletRepository()