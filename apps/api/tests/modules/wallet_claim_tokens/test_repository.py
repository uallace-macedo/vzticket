import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from vzticket.modules.wallet_claim_tokens.model import (
    ClaimTokenStatus,
    WalletClaimToken,
)
from vzticket.modules.wallet_claim_tokens.repository import (
    WalletClaimTokenRepository,
)


@pytest.fixture
def claim_repository(session):
    return WalletClaimTokenRepository(session)


async def test_repository_create_claim_token_success(claim_repository, user):
    now = datetime.now(timezone.utc)
    token_str = str(uuid.uuid4())

    claim_token = WalletClaimToken(
        token=token_str,
        amount=Decimal('50.00'),
        created_at=now,
        expires_at=now + timedelta(minutes=15),
        user_id=user.id,
    )

    saved_token = await claim_repository.create(claim_token)

    assert saved_token.id is not None
    assert saved_token.token == token_str
    assert saved_token.amount == Decimal('50.00')
    assert saved_token.status == ClaimTokenStatus.PENDING


async def test_repository_get_by_token_for_update_success(claim_repository, user):
    now = datetime.now(timezone.utc)
    token_str = str(uuid.uuid4())

    claim_token = WalletClaimToken(
        token=token_str,
        amount=Decimal('100.00'),
        created_at=now,
        expires_at=now + timedelta(minutes=15),
        user_id=user.id,
    )
    await claim_repository.create(claim_token)

    found_token = await claim_repository.get_by_token_for_update(user.id, token_str)

    assert found_token is not None
    assert found_token.token == token_str
    assert found_token.user_id == user.id


async def test_repository_get_pending_by_user(claim_repository, user):
    now = datetime.now(timezone.utc)

    token_pending = WalletClaimToken(
        token=str(uuid.uuid4()),
        amount=Decimal('10.00'),
        created_at=now,
        expires_at=now + timedelta(minutes=15),
        user_id=user.id,
    )
    token_expired = WalletClaimToken(
        token=str(uuid.uuid4()),
        amount=Decimal('20.00'),
        created_at=now - timedelta(minutes=30),
        expires_at=now - timedelta(minutes=15),
        user_id=user.id,
    )

    await claim_repository.create(token_pending)
    await claim_repository.create(token_expired)

    pending_list = await claim_repository.get_pending_by_user(user.id)

    assert len(pending_list) == 1
    assert pending_list[0].token == token_pending.token
