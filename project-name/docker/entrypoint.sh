#!/bin/bash
set -ex

python manage.py collectstatic --noinput

echo "Making migration files"
python manage.py makemigrations --noinput

echo "Migrating Database"
python manage.py migrate --noinput

python manage.py shell < script/create_admin.py

echo "Starting uWSGI"
uwsgi --ini uwsgi.ini

exec "$@"