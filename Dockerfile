FROM python:3.10.2-alpine

WORKDIR /notifications

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install gunicorn && pip install psycopg2-binary


COPY . .

EXPOSE 8080

RUN chmod a+x /notifications/start.sh
# RUN chmod a+x /notifications/celery_worker.sh
# RUN chmod a+x /notifications/celery_beat.sh
# CMD ["/notifications/start.sh"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8080" ]



# CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "notifications.wsgi:application"]