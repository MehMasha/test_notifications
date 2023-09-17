from django.db import models

from apps.clients.models import Client


class Mailing(models.Model):
    """
    Модель рассылки.
    """
    class MailingStatus(models.TextChoices):
        WAITING = 'waiting', 'В ожидании'
        PROGRESS = 'in_progress', 'В процессе'
        DONE = 'done', 'Закончена'

    start_date = models.DateTimeField(
        verbose_name='Дата и время запуска'
    )
    end_date = models.DateTimeField(
        verbose_name='Дата и время конца'
    )
    text = models.TextField(
        verbose_name='Текст рассылки'
    )
    status = models.CharField(
        verbose_name='Статус рассылки',
        choices=MailingStatus.choices,
        default=MailingStatus.WAITING,
        max_length=20
    )

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingFilter(models.Model):
    """
    Модель фильтра рассылки.
    """
    class MailingFilterChoices(models.TextChoices):
        TAG = 'tag', 'Фильтр по тегу'
        MOBILE = 'mobile_code', 'Фильтр по коду оператора'

    mailing = models.ForeignKey(
        to=Mailing,
        on_delete=models.CASCADE,
        verbose_name='Рассылка',
        related_name='mailing_filters'
    )
    filter_type = models.CharField(
        verbose_name='Тип фильтра',
        max_length=100,
        choices=MailingFilterChoices.choices
    )
    value = models.CharField(
        verbose_name='Значение',
        max_length=100
    )

    class Meta:
        verbose_name = 'Фильтр рассылки'
        verbose_name_plural = 'Фильтры рассылок'
        # constraint = UniqueTogether


class Message(models.Model):
    """
    Модель сообщения рассылки.
    """
    class MessageStatus(models.TextChoices):
        SENT = 'sent', 'Отправлено'
        DELIVERED = 'delivered', 'Доставлено'
        ERROR = 'error', 'Ошибка'

    date_send = models.DateTimeField(
        verbose_name='Дата отправки',
        auto_now_add=True
    )
    status = models.CharField(
        verbose_name='Статус сообщения',
        choices=MessageStatus.choices,
        max_length=20
    )
    mailing = models.ForeignKey(
        to=Mailing,
        verbose_name='Рассылка',
        related_name='messages',
        on_delete=models.CASCADE
    )
    client = models.ForeignKey(
        to=Client,
        verbose_name='Клиент',
        related_name='messages',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
