#!/bin/bash
### BEGIN INIT INFO
# Provides:          start_server.sh
# Required-Start:    $all
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Manage the oled server
### END INIT INFO

case "$1" in

    start)
	/root/oled_server/venv/bin/python3 /root/oled_server/main.py&
	exit 0
	;;

    stop)
	/root/oled_server/venv/bin/python3 /root/oled_server/client.py "stop:now"
	exit 0
	;;

    reload|restart)
	;;

    *)
	;;
esac

exit 0
