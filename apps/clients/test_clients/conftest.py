import pytest
from rest_framework.test import APIClient
from apps.clients.models import Client


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
def client_info_new():
    client_info = {
        'phone_number': '79999999998',
        'tag': 'tag1',
        'timezone': '+4'
    }
    return client_info


@pytest.fixture
def mailing_client(client_info):
    client = Client.objects.create(**client_info)
    return client
