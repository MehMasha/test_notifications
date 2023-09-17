import pytest
from django.urls import reverse
from django.utils.dateparse import parse_datetime

from apps.mailing.models import Mailing


def compare_mailings(api_mailing, db_mailing):
    date_fields = ('start_date', 'end_date')
    for field in date_fields:
        assert parse_datetime(api_mailing[field]) == getattr(db_mailing, field)
    other_fields = ('id', 'status', 'text')
    for field in other_fields:
        assert api_mailing[field] == getattr(db_mailing, field)


def compare_mailing_with_form(db_mailing, form_data):
    fields = ('start_date', 'end_date', 'text')
    for field in fields:
        assert form_data[field] == getattr(db_mailing, field)


@pytest.mark.django_db
def test_get_mailings(client, mailing):
    response = client.get(reverse('api:mailing-list'))
    assert response.status_code == 200
    api_mailing = response.json()[0]
    print(api_mailing)
    compare_mailings(api_mailing, mailing)


@pytest.mark.django_db
def test_get_mailing(client, mailing):
    response = client.get(reverse('api:mailing-detail', args=[mailing.id]))
    assert response.status_code == 200
    api_mailing = response.json()
    compare_mailings(api_mailing, mailing)


@pytest.mark.django_db
def test_create_mailing(client, mailing_info):
    response = client.post(
        reverse('api:mailing-list'),
        data=mailing_info
    )
    assert response.status_code == 201
    db_mailing = Mailing.objects.first()
    compare_mailing_with_form(db_mailing, mailing_info)


@pytest.mark.django_db
def test_update_mailing(client, mailing, mailing_info_new):
    response = client.put(
        reverse('api:mailing-detail', args=[mailing.id]),
        data=mailing_info_new
    )
    assert response.status_code == 200
    db_mailing = Mailing.objects.first()
    compare_mailing_with_form(db_mailing, mailing_info_new)


@pytest.mark.django_db
def test_delete_mailing(client, mailing):
    response = client.delete(reverse('api:mailing-detail', args=[mailing.id]))
    assert response.status_code == 204
    assert Mailing.objects.count() == 0


@pytest.mark.django_db
def test_mailings_info(client, mailing, message):
    response = client.get(reverse('api:messages-list', args=[mailing.id]))
    assert response.status_code == 200
    api_message = response.json()[0]
    assert parse_datetime(api_message['date_send']) == getattr(message, 'date_send')
    other_fields = ('id', 'status', )
    for field in other_fields:
        assert api_message[field] == getattr(message, field)
    assert api_message['client'] == message.client.id


@pytest.mark.django_db
def test_mailing_statistic(client, mailing, many_messages):
    response = client.get(reverse('api:mailing-statistic'))
    assert response.status_code == 200
    api_mailing = response.json()[0]
    compare_mailings(api_mailing, mailing)
    assert api_mailing['delivered'] == 1
    assert api_mailing['sent'] == 1
    assert api_mailing['error'] == 1
