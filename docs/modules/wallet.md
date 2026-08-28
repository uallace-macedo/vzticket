# Module Specification: Wallet & Ledger System

## 1. Internal Wallet Ledger Rules

The VzTicket wallet functions as a strict ledger (ledger). The user's balance (`balance`) is never changed directly without a corresponding record in the `wallet_transactions` table.

### Transaction Types & Effects:
- DEPOSIT: Increases user balance (+ amount).
- TICKET_PURCHASE: Decreases user balance (- amount).
- TICKET_REFUND: Increases user balance (+ amount).
- EVENT_CREATION_FEE: Decreases organizer balance (- amount).
- EVENT_PAYOUT: Increases organizer balance (+ net_amount).

---

## 2. PIX Claims & Expiring Tokens

### 2.1 Deposit Flow
1. User requests a deposit of X amount.
2. Server generates a record in `wallet_claim_tokens`:
   - token: Random UUID v4 string.
   - amount: Requested deposit value.
   - type: 'DEPOSIT'
   - expires_at: NOW() + 15 minutes.
   - status: 'PENDING'
3. User scans or reopens the PIX modal via `GET /wallet/pending`.

### 2.2 Confirmation / Claim Endpoint: POST /wallet/claim/{token}
- Validation:
  ```python
  claim_token = await db.execute(
      select(WalletClaimToken)
      .where(WalletClaimToken.token == token)
      .with_for_update()
  )
  if claim_token.status != "PENDING":
      raise HTTPException(status_code=400, detail="Cobrança já processada ou expirada.")
  if claim_token.expires_at < datetime.now(timezone.utc):
      claim_token.status = "EXPIRED"
      raise HTTPException(status_code=400, detail="Cobrança PIX expirada.")
  ```
- Atomic Execution:
  1. Set claim_token.status = 'CLAIMED'.
  2. Increase user.balance += claim_token.amount.
  3. Create record in `wallet_transactions` with type DEPOSIT.

---

## 3. Fee Structure & Calculations

### 3.1 Event Creation Fee (Organizer)
- Fee rate: 5% of ticket_price.
- Action: Debited from organizer balance upon event creation.
- If organizer balance < creation fee, creation fails with HTTP 400.

### 3.2 Convenience Fee (Client)
- Formula: R$ 1.50 + (ticket_price * 0.06)
- Example for R$ 15.00 ticket:
  - Base: 15.00
  - Convenience Fee: 1.50 + (15.00 * 0.06) = 2.40
  - Total charged to client: R$ 17.40

---

## 4. Refund Policy Rules

When a client cancels a ticket via `POST /tickets/{id}/cancel`:

- Condition 1: Up to 7 days after purchase -> 100% full refund to wallet.
- Condition 2: Between 48h and 24h before event_date -> 80% refund to wallet (20% retained).
- Condition 3: Less than 24h before event_date -> Refund disabled (HTTP 400).

---

## 5. Automated Payout Cron Job (D+1)

Routine scheduled via APScheduler running daily at 00:00 UTC.

- Logic:
  1. Fetch all events with event_date in the past day where status is 'ACTIVE'.
  2. Calculate gross_amount = total ticket sales.
  3. Calculate platform_fee_amount = sum of service fees.
  4. Calculate net_amount = gross_amount - platform_fee_amount.
  5. Deposit net_amount into organizer.balance.
  6. Create record in `event_payouts` with status 'PAID'.
  7. Update event.status = 'FINISHED'.
