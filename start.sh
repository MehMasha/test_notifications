#!/bin/sh

until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done
python manage.py collectstatic --noinput
gunicorn --bind 0.0.0.0:8080 notifications.wsgi