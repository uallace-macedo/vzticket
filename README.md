# Livebit 🔨

> Em desenvolvimento

Plataforma de leilões em tempo real construída com Java, Go, Kafka, Angular e WebSocket + autenticação OAuth2/JWT, processamento concorrente de lances e gerenciamento automatizado do ciclo de vida dos leilões.

---

## Serviços

| Serviço | Tech | Responsabilidade |
|---|---|---|
| `livebit-api` | Spring Boot | API principal, autenticação OAuth2/JWT, leilões, WebSocket |
| `livebit-bidder` | Golang | Recebe lances, valida e publica no Kafka |
| `livebit-web` | Angular | Interface em tempo real |
| Kafka | - | Comunicação assíncrona entre serviços |
| PostgreSQL | - | Persistência |
| Redis | - | Cache do lance mais alto por leilão |

---

## Como rodar

```bash
cp .env.example .env
./setup-keys.sh
docker compose up
```

---

## Segurança

- Autenticação via OAuth2 com chaves RSA (.pem)
- JWT com Spring Security
- CORS configurado por ambiente
