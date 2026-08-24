# Requisitos Funcionais do Sistema

---

## Frontend

| ID | Módulo | Descrição |
| :--- | :--- | :--- |
| **RF-FE01** | Catálogo de Eventos | Listagem, busca e filtragem de eventos com status `ACTIVE`. |
| **RF-FE02** | Criação de Evento | Formulário de criação via TMDB ou evento Customizado com validação de CEP e Google Maps. |
| **RF-FE03** | Checkout e Venda | Seleção de quantidade, cálculo de taxa de conveniência e pagamento via Saldo ou PIX. |
| **RF-FE04** | Carteira Digital | Visualização de saldo, extrato com filtros, emissão de depósitos via PIX e exibição de cobranças pendentes. |
| **RF-FE05** | Meus Ingressos | Exibição de ingressos (disponíveis, cancelados e usados), download/compartilhamento e fluxo de cancelamento. |
| **RF-FE06** | Módulo de Portaria | Leitura de QR Code via câmera do dispositivo ou digitação manual do ID. |

---

## Backend

| ID | Módulo | Descrição |
| :--- | :--- | :--- |
| **RF-BE01** | Integração TMDB | Consumo de dados e imagens da API do TMDB para criação simplificada de eventos. |
| **RF-BE02** | Autenticação RBAC | Controle de acesso via JWT com 3 papéis (`CLIENT`, `ORGANIZER`, `GATEKEEPER`). |
| **RF-BE03** | Controle Atômico de Estoque | Decremento de `available_tickets` com lock atômico para evitar *overbooking*. |
| **RF-BE04** | Idempotência no Check-in | Trava transacional para impedir duas validações concorrentes do mesmo ingresso. |
| **RF-BE05** | Motor de Reembolso | Cálculo e estorno proporcional do valor no saldo de acordo com a janela de tempo da compra. |
| **RF-BE06** | Repasse em D+1 (Cron) | Execução via APScheduler para apuração de saldo e liquidação para a carteira do organizador. |
