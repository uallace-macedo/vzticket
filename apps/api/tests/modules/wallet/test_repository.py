"""Persistence tests for the wallet repository."""

import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.modules.auth.models import User, UserRole
from vzticket.modules.wallet.models import (
    ClaimTokenStatus,
    ClaimTokenType,
    TransactionType,
    WalletClaimToken,
    WalletTransaction,
)
from vzticket.modules.wallet.repository import WalletRepository


async def _seed_user(session: AsyncSession) -> User:
    user = User(
        name='Jane Doe',
        email='jane@example.com',
        password_hash='hashed',
        role=UserRole.CLIENT,
        balance=Decimal('100.00'),
        pending_balance=Decimal('0.00'),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def _seed_token(session: AsyncSession, user_id: uuid.UUID) -> WalletClaimToken:
    token = WalletClaimToken(
        token=str(uuid.uuid4()),
        amount=Decimal('50.00'),
        type=ClaimTokenType.DEPOSIT,
        user_id=user_id,
        status=ClaimTokenStatus.PENDING,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=15),
    )
    session.add(token)
    await session.commit()
    await session.refresh(token)
    return token


async def test_get_user_by_id_for_update_locks_row(session: AsyncSession):
    user = await _seed_user(session)

    locked = await WalletRepository(session).get_user_by_id_for_update(user.id)

    assert locked is not None
    assert locked.id == user.id


async def test_get_claim_token_for_update_locks_row(session: AsyncSession):
    user = await _seed_user(session)
    token = await _seed_token(session, user.id)

    locked = await WalletRepository(session).get_claim_token_for_update(token.token)

    assert locked is not None
    assert locked.token == token.token


async def test_get_claim_token_for_update_returns_none_when_missing(
    session: AsyncSession,
):
    locked = await WalletRepository(session).get_claim_token_for_update('missing')

    assert locked is None


async def test_create_claim_token_persists(session: AsyncSession):
    user = await _seed_user(session)
    token = WalletClaimToken(
        token=str(uuid.uuid4()),
        amount=Decimal('50.00'),
        type=ClaimTokenType.DEPOSIT,
        user_id=user.id,
        status=ClaimTokenStatus.PENDING,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=15),
    )

    created = await WalletRepository(session).create_claim_token(token)

    assert created.id is not None
    assert created.status == ClaimTokenStatus.PENDING


async def test_update_token_status_persists(session: AsyncSession):
    user = await _seed_user(session)
    token = await _seed_token(session, user.id)
    repo = WalletRepository(session)

    token.status = ClaimTokenStatus.CLAIMED
    token.claimed_at = datetime.now(timezone.utc)
    await repo.commit()

    await session.refresh(token)
    assert token.status == ClaimTokenStatus.CLAIMED
    assert token.claimed_at is not None


async def test_create_transaction_logs_audit(session: AsyncSession):
    user = await _seed_user(session)
    transaction = WalletTransaction(
        user_id=user.id,
        amount=Decimal('50.00'),
        type=TransactionType.DEPOSIT,
        description='Depósito via cobrança PIX',
    )

    created = await WalletRepository(session).create_transaction(transaction)

    assert created.id is not None
    assert created.amount == Decimal('50.00')


async def test_get_user_transactions_returns_newest_first(session: AsyncSession):
    user = await _seed_user(session)
    repo = WalletRepository(session)

    desc1 = 'Primeiro depósito'
    desc2 = 'Segundo depósito'

    first = WalletTransaction(
        user_id=user.id,
        amount=Decimal('10.00'),
        type=TransactionType.DEPOSIT,
        description=desc1,
    )

    second = WalletTransaction(
        user_id=user.id,
        amount=Decimal('20.00'),
        type=TransactionType.DEPOSIT,
        description='Segundo depósito',
    )
    await repo.create_transaction(first)
    await repo.create_transaction(second)
    await repo.commit()

    transactions = await repo.get_user_transactions(user.id)

    assert len(transactions) == 2
    assert transactions[0].description == desc1
    assert transactions[1].description == desc2


async def test_get_pending_claim_token_returns_pending(session: AsyncSession):
    user = await _seed_user(session)
    token = await _seed_token(session, user.id)

    pending = await WalletRepository(session).get_pending_claim_token(user.id)

    assert pending is not None
    assert pending.token == token.token


async def test_get_pending_claim_token_ignores_claimed(session: AsyncSession):
    user = await _seed_user(session)
    token = await _seed_token(session, user.id)
    repo = WalletRepository(session)
    token.status = ClaimTokenStatus.CLAIMED
    await repo.commit()

    pending = await repo.get_pending_claim_token(user.id)

    assert pending is None