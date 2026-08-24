#!/bin/sh

set -e
export PYTHONPATH=.

echo "⏳ Executando migrations (Alembic)..."
alembic upgrade head

echo "🌱 Executando script de seed..."
python scripts/seed.py

echo "🚀 Iniciando a API..."
exec fastapi run vzticket/main.py --port 8000