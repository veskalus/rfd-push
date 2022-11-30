#!/bin/sh

echo "$(date) Starting rfd-push"

/usr/sbin/crond -f -l 8                   # start cron service
