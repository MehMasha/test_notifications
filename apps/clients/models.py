from django.core.validators import RegexValidator
from django.db import models


class Client(models.Model):
    """
    Модель клиента рассылки.
    """
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
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
