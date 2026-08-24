from uuid import uuid4

import pytest

from vzticket.core.security.types import TokenPayload
from vzticket.modules.users.model import UserRole


@pytest.fixture
def valid_payload():
    return TokenPayload(
        sub=uuid4(),
        email='dev@vzticket.com',
        role=UserRole.CLIENT,
    )
