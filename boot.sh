#!/bin/bash
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done
# exec -it microblog python reindex.py
python -m microblog reindex.py
exec gunicorn -b :5000 --access-logfile - --error-logfile - microblog:app