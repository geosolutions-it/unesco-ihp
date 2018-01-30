#!/usr/bin/env bash

# set -x

source ~/.virtualenvs/geonode/bin/activate

pushd $(dirname $0)

case $1 in
	"backup-file")
		case $2 in
                        "")
                                echo "Missing 'backup-file <backup-file>' path!"
                                ;;
			*)
				echo "Starting Restore from $2"
				DJANGO_SETTINGS_MODULE=ihp.settings python -W ignore manage.py restore --backup-file=$2
				# DJANGO_SETTINGS_MODULE=ihp.settings python -W ignore manage.py migrate_baseurl -f --source-address=ihp-wins-dev.geo-solutions.it --target-address=ihp-wins.unesco.org
				;;
		esac
		;;
	*)
		echo "Missing 'backup-file' parameter!"
		;;
esac

exit 0
