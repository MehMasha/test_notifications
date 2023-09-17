from django.contrib import admin

from apps.mailing.models import Mailing, MailingFilter, Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Message._meta.fields]


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Mailing._meta.fields]


@admin.register(MailingFilter)
class MailingFilterAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MailingFilter._meta.fields]
