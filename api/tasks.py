import requests
from rest_framework import status
from celery import shared_task
from datetime import datetime, timezone, timedelta
from django.db.models import Q
from django.conf import settings
from mailing.models import Mailing, Message, Client


def get_time_now():
    timezone_offset = 3.0
    tzinfo = timezone(timedelta(hours=timezone_offset))
    return datetime.now(tzinfo)


@shared_task
def check_mailings():
    mailings = Mailing.objects.filter(status='waiting').order_by('start_date')
    for mailing in mailings:
        print(mailing)
        now = get_time_now()
        if mailing.start_date <= now <= mailing.end_date:
            mailing.status = Mailing.MailingStatus.PROGRESS
            start_mailing.delay(mailing.id)


@shared_task
def start_mailing(mailing_id: int, clients=None):
    print(mailing_id)
    mailing = Mailing.objects.get(id=mailing_id)
    not_sent_clients = []
    if not clients:
        clients = Client.objects.all()
        mailing_filters = mailing.mailing_filters.all()
        all_filters = {}
        for fil in mailing_filters:
            filter_type = fil.filter_type
            all_filters[filter_type] = all_filters.get(filter_type,
                                                       []) + [fil.value]
        for fil, values in all_filters.items():
            filter_condition = Q(**{fil + '__in': values})
            clients = clients.filter(filter_condition)

    for client in clients:
        now = get_time_now()
        if mailing.end_date <= now:
            mailing.status = Mailing.MailingStatus.DONE
            return
        message = Message.objects.create(
            status=Message.MessageStatus.SENT,
            mailing=mailing,
            client=client
        )
        data = {
            'id': message.id,
            'phone': client.phone_number,
            'text': mailing.text
        }

        response = requests.post(
            settings.SERVICE_URL + f'/send/{message.id}',
            json=data,
            headers=settings.SERVICE_HEADERS
        )
        if response.status_code == status.HTTP_200_OK:
            message.status = Message.MessageStatus.DELIVERED
        else:
            message.status = Message.MessageStatus.ERROR
            not_sent_clients.append(client)
        message.save()

    if not_sent_clients:
        now = get_time_now()
        if mailing.start_date <= now <= mailing.end_date:
            start_mailing(mailing, not_sent_clients)

    mailing.status = Mailing.MailingStatus.DONE
    mailing.save()

# celery worker -A notifications --loglevel=info
# celery -A notifications beat
