import logging
from datetime import datetime, timedelta, timezone

import requests
from celery import shared_task
from django.conf import settings
from django.db.models import Q
from rest_framework import status

from apps.mailing.models import Client, Mailing, Message

logger = logging.getLogger('json_logger')


def get_time_now():
    timezone_offset = 3.0
    tzinfo = timezone(timedelta(hours=timezone_offset))
    return datetime.now(tzinfo)


@shared_task
def check_mailings():
    mailings = Mailing.objects.filter(status='waiting').order_by('start_date')
    for mailing in mailings:
        now = get_time_now()
        if mailing.start_date <= now <= mailing.end_date:
            mailing.status = Mailing.MailingStatus.PROGRESS
            logger.info(
                'Mailing starting now',
                extra={
                    'mailing_id': mailing.id
                }
            )
            start_mailing.delay(mailing.id)


@shared_task
def start_mailing(mailing_id: int, clients=None):
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
            logger.info(
                'Mailing done, time is up',
                extra={
                    'mailing_id': mailing.id,
                }
            )
            return
        message, _ = Message.objects.get_or_create(
            mailing=mailing,
            client=client
        )
        message.save()
        message.status = Message.MessageStatus.SENT
        data = {
            'id': message.id,
            'phone': client.phone_number,
            'text': mailing.text
        }
        logger.info(
            'Sending message to client',
            extra={
                'mailing_id': mailing.id,
                'client_id': client.id,
                'message_id': message.id,
            }
        )
        response = requests.post(
            settings.SERVICE_URL + f'/send/{message.id}',
            json=data,
            headers=settings.SERVICE_HEADERS
        )
        if response.status_code == status.HTTP_200_OK:
            message.status = Message.MessageStatus.DELIVERED
            logger.info(
                'Message delivered',
                extra={
                    'mailing_id': mailing.id,
                    'client_id': client.id,
                    'message_id': message.id,
                }
            )
        else:
            message.status = Message.MessageStatus.ERROR
            not_sent_clients.append(client)
            logger.info(
                'Error sending message',
                extra={
                    'mailing_id': mailing.id,
                    'client_id': client.id,
                    'message_id': message.id,
                }
            )
        message.save()

    if not_sent_clients:
        now = get_time_now()
        if mailing.start_date <= now <= mailing.end_date:
            start_mailing(mailing, not_sent_clients)

    mailing.status = Mailing.MailingStatus.DONE
    logger.info(
        'Mailing done',
        extra={
            'mailing_id': mailing.id,
        }
    )
    mailing.save()
