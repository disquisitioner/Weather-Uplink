### BEGIN INIT INFO
# Provides: Weather Station Feed - Processe sensor data from Arduino and relay to the cloud
# Required-Start: $remote_fs $syslog
# Required-Stop: $remote_fs $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Weather Station feed to the cloud
# Description: Weather Station feed to the cloud (Xively, Voices, &c.)
### END INIT INFO


#! /bin/sh
# /etc/init.d/wxinit

# Author: David Bryant (djbryant@gmail.com)
# Version: 3.0 (June 22, 2013)

export HOME
case "$1" in
    start)
        echo "Starting Weather Station feed"
        /usr/bin/python -u /home/wx/bin/wxstation2web.py > /home/wx/bin/wx.out 2>&1 &
    ;;
    stop)
        echo "Stopping Weather Station feed"
	WXFEED_PID=`ps auxwww | grep wxstation2web.py | head -1 | awk '{print $2}'`
		if [ -z "$WXFEED_PID" ] 
		then
			echo "Weather Station feed was not running..."
		else
				kill -9 $WXFEED_PID
		fi
    ;;
    *)
        echo "Usage: /etc/init.d/wxinit {start|stop}"
        exit 1
    ;;
esac
exit 0
