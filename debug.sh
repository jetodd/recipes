#!/usr/bin/env sh

echo $PATH

which gunicorn

pwd

ls -la

exec gunicorn --bind :8080 --workers 2 recipes.wsgi
