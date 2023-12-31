# Generated by Django 4.2.5 on 2023-09-14 14:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(verbose_name='Дата и время запуска')),
                ('end_date', models.DateTimeField(verbose_name='Дата и время конца')),
                ('text', models.TextField(verbose_name='Текст рассылки')),
                ('status', models.CharField(choices=[('waiting', 'В ожидании'), ('in_progress', 'В процессе'), ('done', 'Закончена')], default='waiting', max_length=20, verbose_name='Статус рассылки')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_send', models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')),
                ('status', models.CharField(choices=[('sent', 'Отправлено'), ('delivered', 'Доставлено'), ('error', 'Ошибка')], max_length=20, verbose_name='Статус сообщения')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='clients.client', verbose_name='Клиент')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='mailing.mailing', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='MailingFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filter_type', models.CharField(choices=[('tag', 'Фильтр по тегу'), ('mobile_code', 'Фильтр по коду оператора')], max_length=100, verbose_name='Тип фильтра')),
                ('value', models.CharField(max_length=100, verbose_name='Значение')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mailing_filters', to='mailing.mailing', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'Фильтр рассылки',
                'verbose_name_plural': 'Фильтры рассылок',
            },
        ),
    ]
