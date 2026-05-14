# Livebit

Plataforma de leiloes em tempo real.

---

## Servicos

1. **`livebit-api:`** quarkus (api principal; autenticacao; leiloes e websocket)
2. **`livebit-bidder:`** golang (recebe lances, valida e publica no kafka)
3. **`livebit-web:`** interface
4. **`kafka`**
5. **`postgresql`**
6. **`redis`**

---

## Como rodar

```bash
cp .env.example .env
docker compose up
```
