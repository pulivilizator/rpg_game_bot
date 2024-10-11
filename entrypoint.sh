#!/bin/sh

alembic upgrade head

python3 nats/migrations.py

if [ $? -eq 0 ]; then
  cd bot
  exec python3 -m bot
else
  echo "Migrations failed. Exiting."
  exit 1
fi