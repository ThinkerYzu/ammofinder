#!/bin/sh
PY=$(dirname $0)/targetsports.py
while true; do
    TM=$(date '+%H:%M.%S')
    echo "$TM Check ammo"
    AVAIL=$(python3 $PY)
    if [ -n "$AVAIL" ]; then
        echo "$AVAIL"
        notify-send "Ammo Available ($TM)" "$AVAIL"
    fi
    sleep 307
done
