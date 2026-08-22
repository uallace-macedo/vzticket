# Requisitos Funcionais do Sistema (vzticket)

Mapeamento completo dos requisitos do Frontend e do Backend por módulo e ID funcional.

---

## Requisitos do Frontend

| ID | Módulo | Descrição |
| :--- | :--- | :--- |
| **RF-FE01** | Catálogo de Eventos | Navegação, busca e filtragem de eventos publicados na plataforma. |
| **RF-FE02** | Gestão de Eventos | Interface para o organizador criar, publicar e configurar eventos. |
| **RF-FE03** | Fluxo de Reserva | Seleção por quantidade de ingressos desejada. |
| **RF-FE04** | Checkout e Pagamento | Fluxo de checkout simulado integrado a PIX e Saldo da Carteira. |
| **RF-FE05** | Meus Ingressos | Área autenticada do cliente que exibe ingressos ativos, detalhes e QR Code. |
| **RF-FE06** | Tela de Portaria | Leitura de QR Code via câmera ou digitação manual de token pelo portador. |
| **RF-FE07** | Feedback de Entrada | Retorno visual na portaria: válido, inválido, utilizado ou evento incorreto. |
| **RF-FE08** | Ingressos em Tempo Real | Atualização e reserva temporária do estoque de ingressos em tempo real. |

---

## Requisitos do Backend

| ID | Módulo | Descrição |
| :--- | :--- | :--- |
| **RF-BE01** | API Externa | Integração de dados com APIs externas (ex: TMDb para cartazes e informações). |
| **RF-BE02** | Autenticação JWT | Login e registro com hash seguro e controle de acesso por papel (`Role`). |
| **RF-BE03** | Prevenção de Overbooking | Garantia atômica no banco de dados para que o número de ingressos vendidos não exceda `available_tickets`. |
| **RF-BE04** | Segurança QR Code | Geração de payloads assinados e criptografados para o QR Code do ingresso. |
| **RF-BE05** | Compartilhamento | Endpoint público para visualização de ingresso via token único sem necessidade de login. |
| **RF-BE06** | Validação Idempotente | Transição estrita para status `USED` no check-in, impedindo reaproveitamento de ingresso. |
| **RF-BE07** | Cancelamento e Devolução | Cancelamento de compra com estorno no saldo e devolução automática do ingresso ao estoque. |
| **RF-BE08** | Gestão de Estoque Atômica | Controle atômico de concurrency ao decrementar `available_tickets` durante a compra. |
