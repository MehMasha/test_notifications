from apps.clients.models import Client
from django.urls import reverse
import pytest


def compare_clients(api_client, db_client):
    for field in Client._meta.fields:
        assert api_client[field.name] == getattr(db_client, field.name)


def compare_client_with_form(db_client, form_data):
    for field in form_data:
        assert getattr(db_client, field) == form_data[field]


@pytest.mark.django_db
def test_get_clients(client, mailing_client):
    response = client.get(reverse('api:clients-list'))
    assert response.status_code == 200
    api_client = response.json()[0]
    compare_clients(api_client, mailing_client)


@pytest.mark.django_db
def test_get_client(client, mailing_client):
    response = client.get(reverse('api:clients-detail', args=[mailing_client.id]))
    assert response.status_code == 200
    api_client = response.json()
    compare_clients(api_client, mailing_client)


@pytest.mark.django_db
def test_create_client(client, client_info_new):
    response = client.post(reverse('api:clients-list'), data=client_info_new)
    assert response.status_code == 201
    db_client = Client.objects.first()
    compare_client_with_form(db_client, client_info_new)


@pytest.mark.django_db
def test_update_client(client, mailing_client, client_info_new):
    response = client.put(
        reverse('api:clients-detail', args=[mailing_client.id]),
        data=client_info_new
    )
    assert response.status_code == 200
    db_client = Client.objects.first()
    compare_client_with_form(db_client, client_info_new)


@pytest.mark.django_db
def test_delete_client(client, mailing_client):
    response = client.delete(reverse('api:clients-detail', args=[mailing_client.id]))
    assert response.status_code == 204
    assert Client.objects.count() == 0
