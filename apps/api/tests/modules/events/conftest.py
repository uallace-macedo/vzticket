from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import uuid4

import pytest

from vzticket.modules.events.schemas import EventCreate


@pytest.fixture
def event_data(organizer_user):
    return EventCreate(
        organizer_id=organizer_user.id,
        title="Show de Rock",
        description="Descrição do show",
        available_tickets=100,
        ticket_price=Decimal("50.00"),
        event_date=datetime.now(timezone.utc) + timedelta(days=5),
        location_name="Espaço das Américas",
        cep="01156-000",
        address="Rua Tagipuru",
        number="795",
        neighborhood="Barra Funda",
        city="São Paulo",
        state="SP",
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
