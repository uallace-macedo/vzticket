# Regras de Negócio e Monetização

## 1. Carteira Digital e Cobranças (PIX)

A aplicação não utiliza gateways externos. O ciclo financeiro é realizado via simulação orquestrada no banco de dados.

* **Depósitos PIX:** Geram um registro na tabela `WALLET_CLAIM_TOKENS` com validade de 15 minutos.
* **Pendências:** Caso o modal de cobrança seja fechado, a cobrança fica visível em `Carteira > Pendências` para reabertura do QR Code ou link antes do tempo de expiração.
* **Confirmação:** A chamada ao endpoint do PIX simula a liquidação, alterando o status do token para `CLAIMED` e incrementando o `balance` do usuário.

---

## 2. Estrutura de Taxas

### 2.1. Taxa de Criação de Evento (Organizador)
* **Valor:** 5% sobre o preço do ingresso (`ticket_price`).
* **Regra:** Para criar o evento, o valor de 5% é debitado da carteira do organizador.
* *Exemplo:* Se o ingresso custa R$ 15,00, a taxa de criação do evento é de R$ 0,75.

### 2.2. Taxa de Emissão de Ingresso (Cliente Final)
* **Fórmula:** `R$ 1.50 + (Preço do Ingresso * 6%)`
* *Exemplo:* Para um ingresso de R$ 15,00:
  $$\text{Taxa} = 1.50 + (15.00 \times 0.06) = 1.50 + 0.90 = \text{R\$ } 2.40$$
  $$\text{Valor Total Pago pelo Cliente} = 15.00 + 2.40 = \text{R\$ } 17.40$$

---

## 3. Política de Reembolso e Cancelamento de Ingressos

O cancelamento pelo cliente pode ser realizado na aba `Meus Ingressos`:

| Prazo do Cancelamento | Percentual do Reembolso ao Cliente | Retenção / Distribuição da Taxa |
| :--- | :--- | :--- |
| **Até 7 dias após a compra** | 100% do valor retoma para a carteira | Sem retenção de taxa |
| **Entre 48h e 24h antes do evento** | 80% do valor retoma para a carteira | Taxa de 20%: 80% repassado ao organizador e 20% mantido pela plataforma |
| **A menos de 24h do evento** | Não é permitido o cancelamento | - |

---

## 4. Criação e Dados do Evento

* **Localização (Obrigatório):** Sanitização do CEP (salvando apenas números) + envio de URL válida do **Google Maps**.
* **Origem dos Dados:**
  * **TMDB:** Dados e mídias (`poster_url` e `banner_url`) buscados diretamente da API.
  * **Custom:** Requer o preenchimento manual e o envio obrigatório do parâmetro `custom_image_url`.
* **Janela de Vendas:** A compra de ingressos só fica disponível entre as datas de `sales_start_at` e `sales_end_at`.

---

## 5. Validação de Ingressos (Portaria)

* **Janela de Permissão:** A validação só é liberada **no dia do evento** (`event_date`), em qualquer horário.
* **Escopo por Perfil:**
  * **Portaria (`GATEKEEPER`):** Pode validar ingressos de qualquer evento cadastrado na plataforma.
  * **Organizador (`ORGANIZER`):** Pode validar apenas os ingressos dos seus próprios eventos.
* **Métodos:** Leitura via câmera (QR Code com hash assinado) ou inserção manual do código/ID do ingresso.
* **Idempotência:** A requisição realiza locking atômico na linha da tabela `TICKETS` para evitar validação duplicada em chamadas simultâneas.

---

## 6. Repasse Financeiro ao Organizador (Payout Cron)

O processamento financeiro é executado automaticamente via **APScheduler**:

1. **Rotina diária (00:00):** O Job verifica os eventos que foram realizados no dia anterior.
2. **Cálculo do Repasse ($D+1$):**
   * Consolidação da receita bruta de vendas.
   * Subtração das taxas da plataforma.
   * Depósito automático da receita líquida na carteira do organizador (`EVENT_PAYOUT`).
