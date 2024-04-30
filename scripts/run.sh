#!/bin/sh

set -e
python manage.py collectstatic --noinput
python manage.py migrate

gunicorn --bind 0.0.0.0:9000 --workers 4 app.wsgi:application