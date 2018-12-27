#!/bin/sh
set +e

while true; do
    curl trnfs.com/pizeropizeropizero || echo "fail";
    sleep 60;
done
