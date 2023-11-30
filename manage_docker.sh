#!/usr/bin/env bash

docker compose -f prod-docker-compose.yaml run --rm nfc-system-manage python manage.py "$@"
