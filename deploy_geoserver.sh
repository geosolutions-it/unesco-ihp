#!/bin/bash

source ~/.virtualenvs/geonode/bin/activate

pushd $(dirname $0)

sudo wget http://build.geonode.org/geoserver/latest/geoserver-2.12.x.war
sudo service tomcat8 stop
sudo rm -Rf /var/lib/tomcat8/webapps/geoserver*
sudo mv geoserver-2.12.x.war /var/lib/tomcat8/webapps/geoserver.war
sudo service tomcat8 restart

exit 0
