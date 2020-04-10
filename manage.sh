#!/bin/bash

source ~/.virtualenvs/geonode3/bin/activate

pushd $(dirname $0)

DJANGO_SETTINGS_MODULE=ihp.settings python manage.py $@

