FROM python:3.8.18-slim

WORKDIR /notifications

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install gunicorn && pip install psycopg2-binary


COPY . .

EXPOSE 8080

RUN chmod a+x /notifications/start.sh
RUN chmod a+x /notifications/celery_worker.sh
RUN chmod a+x /notifications/celery_beat.sh

ENTRYPOINT ["./start.sh"]