# Module Specification: Tickets & Check-in

## 1. Security & Authorization Rules (Fixing IDOR)

### 1.1 Endpoint: GET /api/v1/tickets/{ticket_id}
- Permissions:
  - The ticket owner (ticket.user_id == current_user.id).
  - The event organizer (event.organizer_id == current_user.id).
  - Any active GATEKEEPER.

- Validation Logic:
  ```python
  if current_user.role == "CLIENT" and ticket.user_id != current_user.id:
      raise HTTPException(status_code=403, detail="Acesso não autorizado a este ingresso.")
  ```

- Response Scrubbing:
  - If requested by the owner, return full DTO including the QR Code rendering payload.
  - If requested by an organizer or gatekeeper, exclude sensitive payload data.

---

## 2. QR Code Generation & HMAC Signing

Instead of a plain unverified hash, ticket QR Codes use an HMAC signature to ensure offline/online authenticity.

- HMAC Formula:
  Payload = ticket_id + ":" + event_id + ":" + user_id
  Signature = HMAC-SHA256(SECRET_KEY, Payload)

- Verification Flow:
  1. Gatekeeper scans QR code containing Payload + Signature.
  2. Server re-computes HMAC on payload using SECRET_KEY.
  3. If signatures match, server performs atomic database update with row-locking (FOR UPDATE).

---

## 3. Check-in Concurrency & Idempotency

### Endpoint: POST /api/v1/tickets/{ticket_id}/validate
- Database Transaction:
  ```sql
  SELECT * FROM tickets WHERE id = :ticket_id FOR UPDATE;
  ```

- Rules:
  1. If ticket.status == 'USED', fail immediately with 409 Conflict (detail: "Ingresso já utilizado.").
  2. If ticket.status == 'CANCELLED', fail with 400 Bad Request.
  3. If current date is NOT the event date (event_date), fail with 400 Bad Request (detail: "Validação permitida apenas no dia do evento.").
  4. If valid, set status = 'USED', validated_at = NOW(), and commit transaction.

---

## 4. Required Automated Tests (Pytest)

1. test_get_ticket_idor_protection: Verify a user receives HTTP 403 when trying to access another user's ticket ID.
2. test_checkin_idempotency_concurrent: Simulate two parallel check-in requests for the same ticket using asyncio tasks. Exactly one MUST succeed (HTTP 200) and the other MUST fail (HTTP 409).
3. test_hmac_tampered_signature: Verify that altering the QR payload causes validation to fail with HTTP 400.
