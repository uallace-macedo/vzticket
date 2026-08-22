# Regras de Negócio e Taxas da Plataforma (vzticket)

## 1. Modelo de Taxas e Tarifas

A plataforma opera com duas categorias distintas de taxas de serviço:

### 1.1. Taxa de Publicação de Evento (Organizador)
Cobrada do organizador no momento da criação/publicação do evento.
* **Cálculo:** `EVENT_CREATION_FEE_PERCENTAGE` (ex: 5% ou 8% sobre o preço base do ingresso).
* **Formas de Pagamento:**
  * **Saldo (`BALANCE`):** O valor é debitado imediatamente do `balance` do organizador. O evento nasce com status `ACTIVE`.
  * **PIX:** Gera um token na tabela `WALLET_CLAIM_TOKENS` (`ClaimType.EVENT_FEE`). O evento nasce com status `PENDING_FEE` até a confirmação do pagamento.

### 1.2. Taxa de Emissão de Ingresso (Modelo Híbrido - Cliente)
Cobrada por cada ingresso vendido durante o checkout do comprador/cliente.
* **Fórmula (Modelo 2):**
  $$\text{Taxa do Ingresso} = \text{TICKET\_FEE\_FIXED} + (\text{Preço do Ingresso} \times \text{TICKET\_FEE\_PERCENTAGE})$$
* **Exemplo de Configuração Padrão (`.env`):**
  * `TICKET_FEE_FIXED`: R$ 1.50
  * `TICKET_FEE_PERCENTAGE`: 6% (0.06)

---

## 2. Ciclo de Vida do Evento (`EventStatus`)

| Status | Descrição |
| :--- | :--- |
| `PENDING_FEE` | Evento criado via PIX, aguardando liquidação da taxa de publicação. Não visível no catálogo. |
| `ACTIVE` | Evento publicado, com taxa paga e ingressos disponíveis para compra no catálogo. |
| `CANCELLED` | Evento cancelado pelo organizador ou sistema. Ingressos são estornados (`TICKET_REFUND`). |
| `FINISHED` | Data do evento ultrapassada (`event_date < now()`). Ingressos não podem mais ser validados na portaria. |

---

## 3. Formatação e Higienização de Dados

* **CEP:** Deve ser sanitizado na entrada para salvar apenas números na coluna `cep` (`VARCHAR(9)`). Hífens e pontos são removidos via validator Pydantic (`re.sub(r'\D', '', v)`).
* **Campos Opcionais de Mídia:** `poster_url`, `banner_url` e `custom_image_url` aceitam caminhos relativos de mídia ou URLs completas.
* 