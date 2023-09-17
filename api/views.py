from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins

from api.serializers import (ClientSerializer,
                             MailingSerializer,
                             MessageSerializer)
from mailing.models import Client, Mailing


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class MailingViewSet(viewsets.ModelViewSet):
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()


class MessageViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = MessageSerializer

    def get_queryset(self):
        mailing_id = self.kwargs['mailing_id']
        mailing = get_object_or_404(Mailing, id=mailing_id)
        return mailing.messages.all()
