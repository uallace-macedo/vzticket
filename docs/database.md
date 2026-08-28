# VzTicket - Database Schema Specification

## PostgreSQL Database Diagram

### Table: `users`
- `id`: UUID (Primary Key, default: `gen_random_uuid()`)
- `name`: VARCHAR(100) (Not Null)
- `email`: VARCHAR(255) (Unique, Not Null, Index)
- `password_hash`: VARCHAR(255) (Not Null)
- `role`: ENUM (`'CLIENT'`, `'ORGANIZER'`, `'GATEKEEPER'`) (Not Null, Default: `'CLIENT'`)
- `balance`: NUMERIC(10, 2) (Not Null, Default: `0.00`, Constraint: `>= 0.00`)
- `pending_balance`: NUMERIC(10, 2) (Not Null, Default: `0.00`, Constraint: `>= 0.00`)
- `created_at`: TIMESTAMPTZ (Not Null, Default: `NOW()`)
- `updated_at`: TIMESTAMPTZ (Not Null, Default: `NOW()`)

### Table: `events`
- `id`: UUID (Primary Key, default: `gen_random_uuid()`)
- `organizer_id`: UUID (Foreign Key -> `users.id`, Not Null)
- `title`: VARCHAR(150) (Not Null)
- `description`: TEXT (Not Null)
- `status`: ENUM (`'PENDING_FEE'`, `'ACTIVE'`, `'CANCELLED'`, `'FINISHED'`) (Not Null, Default: `'PENDING_FEE'`)
- `available_tickets`: INT (Not Null, Constraint: `>= 0`)
- `ticket_price`: NUMERIC(10, 2) (Not Null, Constraint: `>= 0.00`)
- `service_fee`: NUMERIC(10, 2) (Not Null, Constraint: `>= 0.00`)
- `ticket_title`: VARCHAR(100) (Not Null, Default: `'Pista'`)
- `ticket_description`: TEXT (Nullable)
- `event_date`: TIMESTAMPTZ (Not Null, Index)
- `sales_start_at`: TIMESTAMPTZ (Nullable)
- `sales_end_at`: TIMESTAMPTZ (Nullable)
- `location_name`: VARCHAR(150) (Not Null)
- `cep`: VARCHAR(8) (Not Null)
- `address`: VARCHAR(255) (Not Null)
- `number`: VARCHAR(20) (Not Null)
- `neighborhood`: VARCHAR(100) (Not Null)
- `city`: VARCHAR(100) (Not Null)
- `city_slug`: VARCHAR(100) (Not Null, Index)
- `state`: VARCHAR(2) (Not Null)
- `complement`: VARCHAR(100) (Nullable)
- `poster_url`: VARCHAR(500) (Nullable)
- `banner_url`: VARCHAR(500) (Nullable)
- `custom_image_url`: VARCHAR(500) (Nullable)
- `maps_url`: VARCHAR(500) (Not Null)
- `created_at`: TIMESTAMPTZ (Not Null, Default: `NOW()`)
- `updated_at`: TIMESTAMPTZ (Not Null, Default: `NOW()`)

### Table: `tickets`
- `id`: UUID (Primary Key, default: `gen_random_uuid()`)
- `event_id`: UUID (Foreign Key -> `events.id`, Not Null)
- `user_id`: UUID (Foreign Key -> `users.id`, Not Null)
- `status`: ENUM (`'VALID'`, `'USED'`, `'CANCELLED'`) (Not Null, Default: `'VALID'`)
- `qr_code_hash`: VARCHAR(255) (Not Null) -- HMAC-SHA256 signature string
- `purchased_at`: TIMESTAMPTZ (Not Null, Default: `NOW()`)
- `validated_at`: TIMESTAMPTZ (Nullable)
- *Indexes*: Composite index on (`user_id`, `status`) and (`event_id`, `status`).

### Table: `wallet_transactions`
- `id`: UUID (Primary Key, default: `gen_random_uuid()`)
- `user_id`: UUID (Foreign Key -> `users.id`, Not Null)
- `event_id`: UUID (Foreign Key -> `events.id`, Nullable)
- `ticket_id`: UUID (Foreign Key -> `tickets.id`, Nullable)
- `type`: ENUM (`'DEPOSIT'`, `'TICKET_PURCHASE'`, `'TICKET_REFUND'`, `'EVENT_CREATION_FEE'`, `'EVENT_PAYOUT'`) (Not Null)
- `amount`: NUMERIC(10, 2) (Not Null)
- `description`: VARCHAR(255) (Not Null)
- `created_at`: TIMESTAMPTZ (Not Null, Default: `NOW()`)

### Table: `wallet_claim_tokens`
- `id`: UUID (Primary Key, default: `gen_random_uuid()`)
- `token`: VARCHAR(255) (Unique, Not Null, Index)
- `amount`: NUMERIC(10, 2) (Not Null)
- `type`: ENUM (`'DEPOSIT'`, `'TICKET_PURCHASE'`, `'EVENT_FEE'`) (Not Null)
- `target_id`: UUID (Nullable)
- `user_id`: UUID (Foreign Key -> `users.id`, Nullable)
- `status`: ENUM (`'PENDING'`, `'CLAIMED'`, `'EXPIRED'`) (Not Null, Default: `'PENDING'`)
- `created_at`: TIMESTAMPTZ (Not Null, Default: `NOW()`)
- `expires_at`: TIMESTAMPTZ (Not Null)
- `claimed_at`: TIMESTAMPTZ (Nullable)

### Table: `event_payouts`
- `id`: UUID (Primary Key, default: `gen_random_uuid()`)
- `event_id`: UUID (Foreign Key -> `events.id`, Unique, Not Null)
- `organizer_id`: UUID (Foreign Key -> `users.id`, Not Null)
- `gross_amount`: NUMERIC(10, 2) (Not Null)
- `platform_fee_amount`: NUMERIC(10, 2) (Not Null)
- `net_amount`: NUMERIC(10, 2) (Not Null)
- `status`: ENUM (`'PENDING'`, `'PROCESSING'`, `'PAID'`, `'FAILED'`) (Not Null, Default: `'PENDING'`)
- `scheduled_for`: TIMESTAMPTZ (Not Null)
- `paid_at`: TIMESTAMPTZ (Nullable)
- `created_at`: TIMESTAMPTZ (Not Null, Default: `NOW()`)
