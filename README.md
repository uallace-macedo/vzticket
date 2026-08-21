# Desafio Elite Dev - Verzel

> *Status: Andamento*

---

Plataforma de eventos e ingressos onde **organizadores** podem criar e gerenciar eventos; **clientes** podem navegar, escolher assentos e quantidades, efetuar pagamentos e receber ingressos como QR Code; equipe de portaria pode validar o QR Code para entrada no evento.

---

## Documentacao do projeto

* [Especificacoes e Requisitos](docs/especificacoes.md): Detalhamento de perfis, requisitos e modelagem de dados


## Carteira Digital (Wallet)

A plataforma possui um sistema de carteira digital interna utilizado para todas as movimentações financeiras da aplicação (criação de eventos, compra e reembolso de ingressos).

### Como Funciona:

1. **Saldo e Extrato:** 
   - Todo usuário possui um saldo (`balance`) associado ao seu perfil.
   - A aba de Carteira exibe o saldo atualizado e o histórico completo de movimentações (`WALLET_TRANSACTIONS`).

2. **Depósito Fictício (PIX):**
   - O usuário pode adicionar saldo simulando um pagamento via PIX (QR Code / Copia e Cola) para realizar transações no sistema.

3. **Taxa de Publicação (Organizador):**
   - Para publicar um evento, é debitada uma taxa fixa (ex: R$ 5,00) diretamente da carteira do organizador.
   - Caso o organizador não possua saldo suficiente, o evento não é publicado até o depósito ser realizado.

4. **Compra de Ingressos (Cliente):**
   - O valor do ingresso é debitado instantaneamente do saldo do cliente no momento do checkout.
   - O cliente pode comprar o ingresso mesmo sem possuir saldo suficiente em sua conta via PIX direto.

5. **Cancelamento e Política de Reembolso:**
   - **Até 7 dias após a compra:** Reembolso integral (100% do valor retorna para o saldo do cliente).
   - **Após 7 dias da compra:** Reembolso parcial de 90% ao cliente. Os 10% restantes são retidos e divididos igualmente entre a plataforma (5%) e o organizador do evento (5%).
