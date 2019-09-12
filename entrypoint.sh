#!/usr/bin/env bash

command="$@"

echo $command | sed --regexp-extended 's/\\(.)/\1/g' | crontab -

crond

trap "echo \"stopping cron\"; kill \$!; exit" SIGINT SIGTERM
cd /epg

python3 /epg/get_data.py - start &&
python3 /epg/get_data.py - fill &&

python3 /epg/web.py
