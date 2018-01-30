#!/bin/bash

pushd $(dirname $0)

./manage.sh dumpdata --indent 2 decat_geonode.hazardalert decat_geonode.hazardtype decat_geonode.alertsourcetype decat_geonode.alertlevel decat_geonode.alertsource -o fixtures/initial_alerts.json


