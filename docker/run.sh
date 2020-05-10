#!/usr/bin/env bash

cd /s106_ms/ || exit 1
python manage.py migrate
python manage.py collectstatic --noinput
daphne -b 0.0.0.0 -p 8088 --access-log /var/log/s106_ms/daphne_access.log MusicShaper.asgi:application
