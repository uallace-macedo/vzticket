from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from vzticket.modules.events.schemas import EventCreate, PaymentMethod


@pytest.fixture
def event_data():
    return EventCreate(
        title="Show de Rock",
        description="Descrição do show de teste bastante completa",
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
        payment_method=PaymentMethod.BALANCE,
    )


@pytest.fixture
def event_payload():
    return {
        "title": "Show de Teste",
        "description": "Descrição do show de teste bastante completa",
        "available_tickets": 50,
        "ticket_price": 75.50,
        "event_date": (datetime.now(timezone.utc) + timedelta(days=10)).isoformat(),
        "location_name": "Teatro Teste",
        "cep": "01310-100",
        "address": "Av. Paulista",
        "number": "1000",
        "neighborhood": "Bela Vista",
        "city": "São Paulo",
        "state": "SP",
        "payment_method": "balance",
    }


@pytest.fixture
async def organizer_with_balance(session, organizer_user):
    organizer_user.balance = Decimal("1000.00")
    session.add(organizer_user)
    await session.commit()
    await session.refresh(organizer_user)
    return organizer_user
