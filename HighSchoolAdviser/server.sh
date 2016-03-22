#!/bin/bash

case "$1" in
"start")
	cd /home/odcdev/ODC.HighSchoolAdviser.Backend/HighSchoolAdviser

        uwsgi --socket /tmp/HighSchoolAdviser.sock --chmod-socket=666 --wsgi-file HighSchoolAdviser/wsgi.py --pidfile=/tmp/HighSchoolAdviser.pid --daemonize /tmp/HighSchoolAdviser.log
;;
"stop")
	uwsgi --stop /tmp/HighSchoolAdviser.pid
;;
"restart")
	$0 stop
	sleep 1
	$0 start
;;
*) echo "Usage: ./server.sh {start|stop|restart}";;
esac

