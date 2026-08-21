from datetime import datetime, timezone
from http import HTTPStatus
from uuid import uuid4

V1_EVENTS_URL = '/api/v1/events'


async def test_create_event_route_success(organizer_client, organizer_user):
    payload = {
        "organizer_id": str(organizer_user.id),
        "title": "Show de Teste",
        "description": "Descrição do show de teste",
        "available_tickets": 50,
        "ticket_price": 75.50,
        "location": "Teatro Teste",
        "event_date": datetime.now(timezone.utc).isoformat(),
        "location_name": "Teatro Teste",
        "cep": "01310-100",
        "address": "Av. Paulista",
        "number": "1000",
        "neighborhood": "Bela Vista",
        "city": "São Paulo",
        "state": "SP"
    }

    response = await organizer_client.post(V1_EVENTS_URL, json=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["title"] == payload["title"]


async def test_search_events_route_success(client):
    response = await client.get(f'{V1_EVENTS_URL}?title=Show&limit=10&offset=0')

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)


async def test_get_event_by_id_not_found(client):
    response = await client.get(f'{V1_EVENTS_URL}/{uuid4()}')

    assert response.status_code == HTTPStatus.NOT_FOUND
