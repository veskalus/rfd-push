#!/bin/sh

/usr/sbin/crond -f -l 8                   # start cron service

#tail -f /dev/null      # keep container running
