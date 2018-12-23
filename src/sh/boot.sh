#!/bin/sh
set -e
cd /home/pi/dev/pizero-led/
echo "Git fetch from pizero-led"
/usr/bin/git fetch
echo "git reset --hard on origin"
/usr/bin/git reset --hard origin/master
exit 0