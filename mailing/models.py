from django.core.validators import RegexValidator
from django.db import models

FILTER_TYPE_CHOICES = (
    ('tag', 'Фильтр по тегу'),
    ('mobile', 'Фильтр по коду оператора'),
)

MESSAGE_STATUS_CHOICES = (
    ('sent', 'Отправлено'),
    ('delivered', 'Доставлено'),
    ('error', 'Ошибка сервера'),
)


class Mailing(models.Model):
    start_date = models.DateTimeField(
        verbose_name='Дата и время запуска'
    )
    end_date = models.DateTimeField(
        verbose_name='Дата и время конца'
    )
    text = models.TextField(
        verbose_name='Текст рассылки'
    )

    class Meta:
        verbose_name = 'Рассылка'


class MailingFilter(models.Model):
    mailing = models.ForeignKey(
        to=Mailing,
        on_delete=models.CASCADE,
        verbose_name='Рассылка',
        related_name='filters'
    )
    filter_type = models.CharField(
        verbose_name='Тип фильтра',
        max_length=100,
        choices=FILTER_TYPE_CHOICES
    )
    filter_value = models.CharField(
        verbose_name='Значение',
        max_length=100
    )

    class Meta:
        verbose_name = 'Фильтр рассылки'


class Client(models.Model):
    phone_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=11,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'7[0-9]{10}$',
                message='Номер телефона должен быть в формате 7XXXXXXXXXX'
            )
        ]
    )
    tag = models.CharField(
        verbose_name='Тэг клиента',
        max_length=20
    )
    timezone = models.CharField(
        verbose_name='Часовой пояс',
        max_length=10
    )

    @property
    def mobile_code(self):
        return self.mobile_code[1:4]
    
    class Meta:
        verbose_name = 'Фильтр рассылки'


class Message(models.Model):
    date_send = models.DateTimeField(
        verbose_name='Дата отправки',
        auto_now_add=True
    )
    status = models.CharField(
        verbose_name='Статус сообщения',
        choices=MESSAGE_STATUS_CHOICES,
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
        verbose_name = 'Сообщения'