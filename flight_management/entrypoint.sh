#!/bin/bash


set -o errexit

python manage.py migrate
python manage.py test --noinput
set +o errexit
python manage.py createsuperuser --noinput

exec "$@"