#!/bin/sh

until cd /notifications
do
    echo "Waiting for server volume..."
done

celery worker -A notifications --loglevel=info
