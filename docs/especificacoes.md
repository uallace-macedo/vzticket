# Especificacoes

## Perfis e Autenticacao

| Papel       | Descricao                                                   |
| ----------- | ----------------------------------------------------------- |
| Organizador | Responsavel por criar e publicar os eventos na plataforma   |
| Cliente     | Usuario final que consome os eventos e adquire ingressos    |
| Portaria    | Operador responsavel pela recepcao e validacao de acesso    |

## Requisitos Funcionais

### Frontend

| ID      | Modulo                 | Descricao                                                            |
| ------- | ---------------------- | -------------------------------------------------------------------- |
| RF-FE01 | Catalogo de Eventos    | Navegacao, busca e filtragem de eventos publicados                   |
| RF-FE02 | Gestao de Eventos      | Interface para organizador criar e configurar eventos                |
| RF-FE03 | Fluxo de Reserva       | Selecao por quantidade de ingressos                                  |
| RF-FE04 | Checkout e Pagamento   | Fluxo de pagamento simulado                                          |
| RF-FE05 | Meus ingressos         | Area autenticada do cliente que exibe o ingresso, detalhes e qrcode  |
| RF-FE06 | Tela de Portaria       | Leitura de QR Code via camera/digitacao manual de token              |
| RF-FE07 | Feedback de Entrada    | Retorno na portaria: valido, invalido, utilizado ou evento errado    |
| RF-FE08 | Assentos em tempo real | Atualizacao da disponibilidade de assentos durante a selecao         |

### Backend
| ID      | Modulo                   | Descricao                                                                                  |
| ------- | ------------------------ | ------------------------------------------------------------------------------------------ |
| RF-BE01 | API Externa              | Integracao com TMDb ou Ticketmaster                                                        |
| RF-BE02 | Autenticacao JWT         | Login/Registro com hash seguro e autenticacao baseada nos 3 papeis                         |
| RF-BE03 | Prevencao de Overbooking | Garantia atomica no banco de dados de que um assento nao sera vendido 2 vezes              |
| RF-BE04 | Seguranca QR Code        | Geracao de QR Code usando payload assinado                                                 |
| RF-BE05 | Compartilhamento         | Endpoint publico para visualizar ingresso atraves de link unico sem login                  |
| RF-BE06 | Validacao Idempotente    | Garantia de que um ingresso transicione para `USED` e nao possa ser revalidado             |
| RF-BE07 | Cancelamento e devolucao | Permitir o cancelamento do ingresso devolvenvo a vaga ao estoque antes do inicio do evento |
| RF-BE08 | Assentos em tempo real   | Atualizacao da disponibilidade de assentos durante a selecao                               |

## Modelagem de dados

```mermaid
erDiagram
  USERS ||--o{ EVENTS : "organizes"
  USERS ||--o{ TICKETS : "purchases"
  USERS ||--o{ WALLET_TRANSACTIONS : "has"
  USERS ||--o{ WALLET_CLAIM_TOKENS : "creates_or_claims"
  EVENTS ||--o{ TICKETS : "has"
  EVENTS ||--o{ WALLET_TRANSACTIONS : "relates_to"
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
    decimal service_fee "Numeric(10, 2) - Default: 2.80"
    string ticket_title "Ex: Entrada Geral"
    text ticket_description "NULLABLE"
    
    datetime event_date
    datetime sales_start_at "NULLABLE"
    datetime sales_end_at "NULLABLE"

    string location_name
    string cep
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
    string maps_url "NULLABLE"
    
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
    enum type "DEPOSIT | "TICKET_PURCHASE | EVENT_FEE"
    uuid target_id "NULLABLE"
    uuid user_id FK "NULLABLE"
    datetime claimed_at "NULLABLE"
    enum status "PENDING | CLAIMED | EXPIRED"
  }
```
