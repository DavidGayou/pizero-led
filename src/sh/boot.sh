#!/bin/sh
set -e
cd /home/pi/dev/pizero-led/
sleep 10
echo "Git fetch from pizero-led"
/usr/bin/git fetch
echo "git reset --hard on origin"
/usr/bin/git reset --hard origin/master

nohup sudo PYTHONPATH=".:build/lib.linux-armv7l-2.7"  python /home/pi/dev/pizero-led/src/python/ledcontroller.py  >/home/pi/dev/pizero-led/run.log 2>&1
exit 0