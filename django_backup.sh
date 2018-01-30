#!/usr/bin/env bash

# set -x

source ~/.virtualenvs/geonode/bin/activate

pushd $(dirname $0)

case $1 in
	"backup-dir")
		case $2 in
                        "")
                                echo "Missing 'backup-dir <backup-dis>' path!"
                                ;;
			*)
				echo "Starting Backup to $2"
				DJANGO_SETTINGS_MODULE=ihp.settings python -W ignore manage.py backup --backup-dir=$2
				;;
		esac
		;;
	*)
		echo "Missing 'backup-dir' parameter!"
		;;
esac

exit 0
