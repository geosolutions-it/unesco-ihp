#!/bin/bash

source ~/.virtualenvs/geonode/bin/activate

pushd $(dirname $0)

DJANGO_SETTINGS_MODULE=ihp.settings python -W ignore manage.py makemigrations --merge
DJANGO_SETTINGS_MODULE=ihp.settings python -W ignore manage.py makemigrations
DJANGO_SETTINGS_MODULE=ihp.settings python -W ignore manage.py migrate
DJANGO_SETTINGS_MODULE=ihp.settings python -W ignore manage.py collectstatic --noinput

touch ihp/wsgi.py

exit 0
