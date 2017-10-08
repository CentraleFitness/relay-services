#!/bin/bash
### BEGIN INIT INFO
# Provides:          <your script name>
# Required-Start:    $all
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Manage my cool stuff
### END INIT INFO

case "$1" in

    start)
	/root/oled/venv/bin/python3 /root/oled/main.py
	exit 0
	;;

    stop)
	/root/oled/venv/bin/python3 /root/oled/main.py stop
	exit 0
	;;

    reload|restart)
	;;

    *)
	;;
esac

exit 0
