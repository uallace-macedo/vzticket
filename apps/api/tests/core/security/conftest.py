from uuid import uuid4

import pytest

from verzel.core.security.types import TokenPayload
from verzel.modules.users.model import UserRole


@pytest.fixture
def valid_payload():
    return TokenPayload(
        sub=uuid4(),
        email='dev@verzel.com',
        role=UserRole.CLIENT,
    )
