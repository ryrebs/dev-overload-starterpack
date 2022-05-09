#!/bin/bash

echo 'Running server gunicorn'

source /absolute/path/env/bin/activate
pip install -r /absolute/path/web/requirements/production.txt

# git push makes file un-executable
# copy these files to the project path
cp -p /absolute/path/gunicorn_start /absolute/path/manage.py /absolute/path/manage_production.py /absolute/path/web
/absolute/path/web/manage_production.py collectstatic --noinput
/absolute/path/web/manage_production.py makemigrations
/absolute/path/web/ manage_production.py migrate
/absolute/path/web/manage_production.py gunicorn_start


# daphne commands
daphne -u /absolute/path/run/daphne.sock config.asgi:channel_layer

# worker
/absolute/path/manage_production.py worker