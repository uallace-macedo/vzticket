"""Unit tests for the wallet service business logic."""

import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from vzticket.modules.auth.models import User, UserRole
from vzticket.modules.wallet.exceptions import (
    ClaimTokenAlreadyUsedError,
    ExpiredClaimTokenError,
    InvalidClaimTokenError,
)
from vzticket.modules.wallet.models import (
    ClaimTokenStatus,
    ClaimTokenType,
    WalletClaimToken,
)
from vzticket.modules.wallet.service import WalletService


def _make_user(user_id: uuid.UUID) -> User:
    return User(
        id=user_id,
        name='Jane Doe',
        email='jane@example.com',
        password_hash='hashed',
        role=UserRole.CLIENT,
        balance=Decimal('100.00'),
        pending_balance=Decimal('0.00'),
    )


def _make_token(
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


async def test_create_deposit_claim_generates_pending_token(
    fake_wallet_repository,
):
    service = WalletService(repository=fake_wallet_repository)
    user_id = uuid.uuid4()

    token = await service.create_deposit_claim(user_id, Decimal('50.00'))

    assert token.token
    assert token.amount == Decimal('50.00')
    assert token.type == ClaimTokenType.DEPOSIT
    assert token.status == ClaimTokenStatus.PENDING
    assert token.user_id == user_id
    assert token.expires_at > datetime.now(timezone.utc)


async def test_claim_token_credits_balance(fake_wallet_repository):
    service = WalletService(repository=fake_wallet_repository)
    user_id = uuid.uuid4()
    user = _make_user(user_id)
    fake_wallet_repository.add_user(user)
    token = _make_token(
        user_id,
        status=ClaimTokenStatus.PENDING,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=15),
    )
    await fake_wallet_repository.create_claim_token(token)

    transaction = await service.claim_token(token.token, user_id)

    assert transaction.amount == Decimal('50.00')
    assert user.balance == Decimal('150.00')
    assert token.status == ClaimTokenStatus.CLAIMED
    assert token.claimed_at is not None


async def test_claim_expired_token_raises(fake_wallet_repository):
    service = WalletService(repository=fake_wallet_repository)
    user_id = uuid.uuid4()
    user = _make_user(user_id)
    fake_wallet_repository.add_user(user)
    token = _make_token(
        user_id,
        status=ClaimTokenStatus.PENDING,
        expires_at=datetime.now(timezone.utc) - timedelta(minutes=1),
    )
    await fake_wallet_repository.create_claim_token(token)

    with pytest.raises(ExpiredClaimTokenError):
        await service.claim_token(token.token, user_id)

    assert token.status == ClaimTokenStatus.EXPIRED


async def test_claim_already_used_token_raises(fake_wallet_repository):
    service = WalletService(repository=fake_wallet_repository)
    user_id = uuid.uuid4()
    user = _make_user(user_id)
    fake_wallet_repository.add_user(user)
    token = _make_token(
        user_id,
        status=ClaimTokenStatus.CLAIMED,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=15),
    )
    await fake_wallet_repository.create_claim_token(token)

    with pytest.raises(ClaimTokenAlreadyUsedError):
        await service.claim_token(token.token, user_id)


async def test_claim_unknown_token_raises(fake_wallet_repository):
    service = WalletService(repository=fake_wallet_repository)
    user_id = uuid.uuid4()
    user = _make_user(user_id)
    fake_wallet_repository.add_user(user)

    with pytest.raises(InvalidClaimTokenError):
        await service.claim_token('unknown-token', user_id)


async def test_claim_token_of_other_user_raises(fake_wallet_repository):
    service = WalletService(repository=fake_wallet_repository)
    owner_id = uuid.uuid4()
    other_id = uuid.uuid4()
    fake_wallet_repository.add_user(_make_user(owner_id))
    fake_wallet_repository.add_user(_make_user(other_id))
    token = _make_token(
        owner_id,
        status=ClaimTokenStatus.PENDING,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=15),
    )
    await fake_wallet_repository.create_claim_token(token)

    with pytest.raises(InvalidClaimTokenError):
        await service.claim_token(token.token, other_id)


async def test_get_balance_returns_amounts(fake_wallet_repository):
    service = WalletService(repository=fake_wallet_repository)
    user_id = uuid.uuid4()
    fake_wallet_repository.add_user(_make_user(user_id))

    balance = await service.get_balance(user_id)

    assert balance['balance'] == Decimal('100.00')
    assert balance['pending_balance'] == Decimal('0.00')