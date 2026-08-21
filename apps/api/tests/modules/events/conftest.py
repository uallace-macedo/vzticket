from datetime import datetime, timezone
from uuid import uuid4

import pytest

from vzticket.modules.events.schemas import EventCreate


@pytest.fixture
def event_data():
    return EventCreate(
        organizer_id=uuid4(),
        title="Show de Rock",
        description="Um show incrível",
        available_tickets=100,
        ticket_price=50.0,
        location="Arena Central",
        event_date=datetime.now(timezone.utc),
    )


@pytest.fixture
def event_payload():
    return {
        "organizer_id": str(uuid4()),
        "title": "Show de Teste",
        "description": "Descrição do show de teste",
        "available_tickets": 50,
        "ticket_price": 75.50,
        "location": "Teatro Teste",
        "event_date": datetime.now(timezone.utc).isoformat(),
    }
