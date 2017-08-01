#!/bin/bash

source ~/.virtualenvs/geonode/bin/activate

pushd $(dirname $0)

DJANGO_SETTINGS_MODULE=ihp.settings python manage.py $1

