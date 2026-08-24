# Arquitetura e Modelagem de Dados

Visão geral do modelo de dados do sistema **VzTicket**, relacionamentos e restrições da base de dados.

---

## Diagrama Entidade-Relacionamento (ER)

```mermaid
erDiagram
  USERS ||--o{ EVENTS : "organizes"
  USERS ||--o{ TICKETS : "purchases"
  USERS ||--o{ WALLET_TRANSACTIONS : "has"
  USERS ||--o{ WALLET_CLAIM_TOKENS : "creates_or_claims"
  USERS ||--o{ EVENT_PAYOUTS : "receives"
  EVENTS ||--o{ TICKETS : "has"
  EVENTS ||--o{ WALLET_TRANSACTIONS : "relates_to"
  EVENTS ||--o| EVENT_PAYOUTS : "generates"
  TICKETS ||--o{ WALLET_TRANSACTIONS : "relates_to"

  USERS {
    uuid id PK
    string name
    string email UK
    enum role "ORGANIZER | CLIENT | GATEKEEPER"
    decimal balance "Numeric(10, 2) - Saldo disponível"
    decimal pending_balance "Numeric(10, 2) - Saldo retido de eventos"
  }

  EVENTS {
    uuid id PK
    uuid organizer_id FK
    string title
    text description
    enum status "PENDING_FEE | ACTIVE | CANCELLED | FINISHED"
    
    int available_tickets
    decimal ticket_price "Numeric(10, 2)"
    decimal service_fee "Numeric(10, 2) - Taxa de serviço por ingresso"
    string ticket_title "Ex: Pista"
    text ticket_description "NULLABLE"
    
    datetime event_date
    datetime sales_start_at "NULLABLE"
    datetime sales_end_at "NULLABLE"

    string location_name
    string cep "VARCHAR(8) - Apenas números"
    string address
    string number
    string neighborhood
    string city
    string city_slug "INDEX"
    string state
    string complement "NULLABLE"
    
    string poster_url "NULLABLE"
    string banner_url "NULLABLE"
    string custom_image_url "NULLABLE"
    string maps_url
    
    datetime created_at
    datetime updated_at
  }

  TICKETS {
    uuid id PK
    uuid event_id FK
    uuid user_id FK
    enum status "VALID | USED | CANCELLED"
    text qr_code_hash
    uuid share_token UK
    datetime purchased_at
    datetime validated_at "NULLABLE"
  }

  WALLET_TRANSACTIONS {
    uuid id PK
    uuid user_id FK
    uuid event_id FK "NULLABLE"
    uuid ticket_id FK "NULLABLE"
    enum type "DEPOSIT | TICKET_PURCHASE | TICKET_REFUND | EVENT_CREATION_FEE | EVENT_PAYOUT"
    decimal amount "Numeric(10, 2)"
    string description
    datetime created_at
  }

  WALLET_CLAIM_TOKENS {
    uuid id PK
    string token UK "UUID v4"
    decimal amount "Numeric(10, 2)"
    datetime created_at
    datetime expires_at
    enum type "DEPOSIT | TICKET_PURCHASE | EVENT_FEE"
    uuid target_id "NULLABLE"
    uuid user_id FK "NULLABLE"
    datetime claimed_at "NULLABLE"
    enum status "PENDING | CLAIMED | EXPIRED"
  }

  EVENT_PAYOUTS {
    uuid id PK
    uuid event_id FK UK
    uuid organizer_id FK
    decimal gross_amount "Numeric(10, 2)"
    decimal platform_fee_amount "Numeric(10, 2)"
    decimal net_amount "Numeric(10, 2)"
    enum status "PENDING | PROCESSING | PAID | FAILED"
    datetime scheduled_for
    datetime paid_at "NULLABLE"
    datetime created_at
  }
```