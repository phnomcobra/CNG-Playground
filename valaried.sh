# chkconfig: 345 13 87
# description: valaried is the ValARIE Service daemon. \

# Source function library.
. /etc/init.d/functions

VALARIED_DIR=/opt/valarie
PIDFILE=$VALARIED_DIR/pid

start() {
        echo -n "Starting ValARIE Server: "
        if [ -f $PIDFILE ]; then
                PID=`cat $PIDFILE`
                echo valaried already running: $PID
                exit 2;
        else
                cd $VALARIED_DIR
                ./python start.py 1>/dev/null 2>/dev/null &
                echo $! > $PIDFILE
                RETVAL=0
                echo
                [ $RETVAL -eq 0 ] && touch /var/lock/subsys/valaried
                return $RETVAL
        fi

}

stop() {
        echo -n "Shutting down ValARIE Server: "
        echo
        kill -9 $(cat $PIDFILE)
        echo
        rf -f $PIDFILE
        rm -f /var/lock/subsys/valaried
        return 0
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)
        status valaried
        ;;
    restart)
        stop
        start
        ;;
    *)
        echo "Usage:  {start|stop|status|restart}"
        exit 1
        ;;
esac
exit $?
