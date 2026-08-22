import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from vzticket.modules.wallet_claim_tokens.exceptions import (
    TokenAlreadyClaimedError,
    TokenExpiredError,
    TokenNotFoundError,
)
from vzticket.modules.wallet_claim_tokens.model import (
    ClaimTokenStatus,
    WalletClaimToken,
)
from vzticket.modules.wallet_claim_tokens.schemas import (
    ClaimTokenClaim,
    ClaimTokenCreate,
)
from vzticket.modules.wallet_claim_tokens.service import WalletClaimTokenService


@pytest.fixture
def claim_service(session):
    return WalletClaimTokenService(session)


async def test_service_create_claim_token_success(claim_service, user):
    data = ClaimTokenCreate(amount=Decimal('30.00'))

    result = await claim_service.create_claim_token(user.id, data)

    assert result.id is not None
    assert result.amount == Decimal('30.00')
    assert result.user_id == user.id
    assert result.status == ClaimTokenStatus.PENDING


async def test_service_claim_token_success(claim_service, user):
    initial_balance = user.balance
    claim_amount = Decimal('50.00')

    create_data = ClaimTokenCreate(amount=claim_amount)
    created_token = await claim_service.create_claim_token(user.id, create_data)

    claim_payload = ClaimTokenClaim(token=created_token.token)
    result = await claim_service.claim_token(claim_payload, user)

    assert result.status == ClaimTokenStatus.CLAIMED
    assert result.claimed_at is not None
    assert user.balance == initial_balance + claim_amount


async def test_service_claim_token_not_found(claim_service, user):
    claim_payload = ClaimTokenClaim(token=str(uuid.uuid4()))

    with pytest.raises(TokenNotFoundError):
        await claim_service.claim_token(claim_payload, user)


async def test_service_claim_token_already_claimed(claim_service, user):
    create_data = ClaimTokenCreate(amount=Decimal('20.00'))
    created_token = await claim_service.create_claim_token(user.id, create_data)

    claim_payload = ClaimTokenClaim(token=created_token.token)
    await claim_service.claim_token(claim_payload, user)

    with pytest.raises(TokenAlreadyClaimedError):
        await claim_service.claim_token(claim_payload, user)


async def test_service_claim_token_expired(claim_service, user):
    now = datetime.now(timezone.utc)
    token_str = str(uuid.uuid4())

    expired_token = WalletClaimToken(
        token=token_str,
        amount=Decimal('20.00'),
        created_at=now - timedelta(minutes=30),
        expires_at=now - timedelta(minutes=15),
        user_id=user.id,
    )
    claim_service.session.add(expired_token)
    await claim_service.session.commit()

    claim_payload = ClaimTokenClaim(token=token_str)

    with pytest.raises(TokenExpiredError):
        await claim_service.claim_token(claim_payload, user)
