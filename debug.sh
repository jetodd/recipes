#!/usr/bin/env sh

echo $PATH

find / -name gunicorn

ls -la /usr/local/bin/

which gunicorn || echo "gunicorn not found"

pwd

ls -la

exec gunicorn --bind :8080 --workers 2 recipes.wsgi
