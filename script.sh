#!/bin/sh

#run this script by cron

echo "$(date) :: We will run rfd search '$SEARCH_TERM' --pages 10 --output json > pulled.list"
/usr/local/bin/rfd search $SEARCH_TERM --pages 10 --output json > pulled.list

echo "$(date) :: Exit code: $?"
echo "$(date) :: Now run parser and notification script."

/usr/local/bin/python3 $DIRPATH/newdealchecker.py

echo "$(date) :: Exit code: $?"


