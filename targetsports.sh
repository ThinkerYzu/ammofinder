#!/bin/sh
PY=$(dirname $0)/targetsports.py
OLD_CONTENT=
while true; do
    TM=$(date '+%H:%M.%S')
    echo "$TM Check ammo"
    AVAIL=$(python3 $PY)
    if [ -n "$AVAIL" ]; then
        echo "$AVAIL"
        if [ x"$OLD_CONTENT" != x"$AVAIL" ]; then
            notify-send "Ammo Available ($TM)" "$AVAIL"
            if echo "$AVAIL" | grep '22lr:' > /dev/null; then
                firefox -private-window https://www.targetsportsusa.com/SignIn.aspx
            fi
        fi
    fi
    OLD_CONTENT="$AVAIL"
    sleep 137
done
