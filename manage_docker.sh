#!/usr/bin/env bash

docker compose -f prod-docker-compose.yaml run --rm screen-system-manage python manage.py "$@"
