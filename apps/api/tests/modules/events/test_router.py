from decimal import Decimal
from http import HTTPStatus
from uuid import uuid4

V1_EVENTS_URL = '/api/v1/events'


async def test_create_event_route_success(
    organizer_client, organizer_with_balance, event_payload
):
    response = await organizer_client.post(V1_EVENTS_URL, json=event_payload)

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()
    assert data["event"]["title"] == event_payload["title"]
    assert data["event"]["location"]["name"] == event_payload["location_name"]
    assert data["event"]["ticket_info"]["ticket_price"] == event_payload["ticket_price"]
    assert data["payment_method"] == "balance"


async def test_create_event_route_pix_success(
    organizer_client, organizer_user, event_payload
):
    event_payload["payment_method"] = "pix"

    response = await organizer_client.post(V1_EVENTS_URL, json=event_payload)

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()
    assert data["payment_method"] == "pix"
    assert data["payment_token"] is not None
    assert data["event"]["status"] == "pending_fee"


async def test_create_event_insufficient_balance(
    organizer_client, organizer_user, session, event_payload
):
    organizer_user.balance = Decimal("0.00")
    session.add(organizer_user)
    await session.commit()

    response = await organizer_client.post(V1_EVENTS_URL, json=event_payload)

    assert response.status_code == HTTPStatus.PAYMENT_REQUIRED


async def test_search_events_route_success(client):
    response = await client.get(f'{V1_EVENTS_URL}?title=Show&limit=10&offset=0')

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)


async def test_get_event_by_id_not_found(client):
    response = await client.get(f'{V1_EVENTS_URL}/{uuid4()}')

    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_get_event_by_id_success(
    client, organizer_with_balance, session, event_data
):
    from vzticket.modules.events.service import EventService

    service = EventService(session)
    created_response = await service.create(organizer_with_balance, event_data)

    response = await client.get(f'{V1_EVENTS_URL}/{created_response.event.id}')

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["id"] == str(created_response.event.id)
    assert data["location"]["city"] == "São Paulo"
