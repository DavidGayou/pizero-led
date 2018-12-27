#!/bin/sh
set -e
cd /home/pi/dev/pizero-led/
sleep 10
echo "Launched boot.sh" >> /home/pi/dev/pizero-led/boot.log
curl trnfs.com/thisispizero

echo "Git fetch from pizero-led" >> /home/pi/dev/pizero-led/boot.log
/usr/bin/git fetch
echo "git reset --hard on origin" >> /home/pi/dev/pizero-led/boot.log
/usr/bin/git reset --hard origin/master

nohup sudo PYTHONPATH=".:build/lib.linux-armv7l-2.7"  python /home/pi/dev/pizero-led/src/python/ledcontroller.py  >/home/pi/dev/pizero-led/run.log 2>&1
exit 0