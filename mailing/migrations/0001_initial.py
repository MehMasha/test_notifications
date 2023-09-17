# Generated by Django 4.2.5 on 2023-09-07 17:45

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator(message='Номер телефона должен быть в формате 7XXXXXXXXXX', regex='7[0-9]{10}$')], verbose_name='Номер телефона')),
                ('tag', models.CharField(max_length=20, verbose_name='Тэг клиента')),
                ('timezone', models.CharField(max_length=10, verbose_name='Часовой пояс')),
            ],
            options={
                'verbose_name': 'Фильтр рассылки',
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(verbose_name='Дата и время запуска')),
                ('end_date', models.DateTimeField(verbose_name='Дата и время конца')),
                ('text', models.TextField(verbose_name='Текст рассылки')),
            ],
            options={
                'verbose_name': 'Рассылка',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_send', models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')),
                ('status', models.CharField(choices=[('sent', 'Отправлено'), ('delivered', 'Доставлено'), ('error', 'Ошибка сервера')], max_length=20, verbose_name='Статус сообщения')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='mailing.client', verbose_name='Клиент')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='mailing.mailing', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='MailingFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filter_type', models.CharField(choices=[('tag', 'Фильтр по тегу'), ('mobile', 'Фильтр по коду оператора')], max_length=100, verbose_name='Тип фильтра')),
                ('filter_value', models.CharField(max_length=100, verbose_name='Значение')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filters', to='mailing.mailing', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'Фильтр рассылки',
            },
        ),
    ]
