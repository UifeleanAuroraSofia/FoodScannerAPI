#!/usr/bin/env bash
# entrypoint.sh

# 1. Apelăm migrațiile
python manage.py migrate --noinput

# 2. Pornim serverul Gunicorn
gunicorn FoodScannerAPI.wsgi:application --bind 0.0.0.0:$PORT --timeout 120