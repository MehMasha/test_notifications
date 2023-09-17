import pytest
from rest_framework.test import APIClient
from apps.mailing.models import Mailing, MailingFilter, Message
from apps.clients.models import Client
from datetime import datetime, timedelta, timezone


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def client_info():
    client_info = {
        'phone_number': '79999999999',
        'tag': 'tag',
        'timezone': '+3'
    }
    return client_info


@pytest.fixture
def mailing_client(client_info):
    client = Client.objects.create(**client_info)
    return client


@pytest.fixture
def many_mailing_clients():
    client1 = Client(phone_number='79999999998', tag='tag', timezone='+3')
    client2 = Client(phone_number='79999999997', tag='tag', timezone='+3')
    client3 = Client(phone_number='79999999996', tag='tag', timezone='+3')
    clients = Client.objects.bulk_create([client1, client2, client3])
    return clients


@pytest.fixture
def mailing_info():
    mailing_info = {
        'start_date': datetime.now(timezone.utc),
        'end_date': datetime.now(timezone.utc) + timedelta(hours=1),
        'text': 'Очень информативная рассылка',
        "mailing_filters": [
            {
                "filter_type": "tag",
                "value": "tag"
            },
            {
                "filter_type": "mobile_code",
                "value": "999"
            },
        ]
    }
    return mailing_info


@pytest.fixture
def mailing_info_new():
    mailing_info = {
        'start_date': datetime.now(timezone.utc) + timedelta(hours=2, days=31),
        'end_date': datetime.now(timezone.utc) + timedelta(hours=3),
        'text': 'Очень информативная рассылка 2',
        "mailing_filters": [
            {
                "filter_type": "tag",
                "value": "tag"
            },
            {
                "filter_type": "tag",
                "value": "tag1"
            },
        ]
    }
    return mailing_info


@pytest.fixture
def mailing(mailing_info):
    mailing_filters = mailing_info['mailing_filters']
    del mailing_info['mailing_filters']
    mailing = Mailing.objects.create(**mailing_info)
    for fil in mailing_filters:
        MailingFilter.objects.create(mailing=mailing, **fil)
    return mailing


@pytest.fixture
def message(mailing, mailing_client):
    message = Message.objects.create(
        mailing=mailing,
        client=mailing_client,
        status=Message.MessageStatus.DELIVERED
    )
    return message


@pytest.fixture
def many_messages(mailing, many_mailing_clients):
    message1 = Message(client=many_mailing_clients[0], mailing=mailing,
                       status=Message.MessageStatus.SENT)
    message2 = Message(client=many_mailing_clients[1], mailing=mailing,
                       status=Message.MessageStatus.DELIVERED)
    message3 = Message(client=many_mailing_clients[2], mailing=mailing,
                       status=Message.MessageStatus.ERROR)
    messages = Message.objects.bulk_create([message1, message2, message3])
    return messages
