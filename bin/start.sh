#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")"/.. && pwd)"
cd "$PROJECT_DIR"

# Python venv
if [ ! -d .venv ]; then
	python3 -m venv .venv
fi

. .venv/bin/activate

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Env file
if [ ! -f .env ]; then
	cp -n .env.example .env || true
fi

# Migrate and sync
python manage.py migrate
python manage.py sync_customers_users || true
python manage.py recalc_balances || true

# Run server
python manage.py runserver 0.0.0.0:8000