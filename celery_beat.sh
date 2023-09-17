#!/bin/sh

until cd /notifications
do
    echo "Waiting for server volume..."
done

# run a worker :)
celery -A notifications beat