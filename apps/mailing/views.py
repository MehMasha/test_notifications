from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.mailing.models import Mailing, Message
from apps.mailing.serializers import (MailingSerializer,
                                      MailingStatisticSerializer,
                                      MessageSerializer)


class MailingViewSet(viewsets.ModelViewSet):
    """
    Эндпоинты для информации по рассылкам.

    Позволяют получить информацию по одному или нескольким рассылкам,
    изменять их или удалять
    """
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()

    @action(detail=False, methods=['get'])
    def statistic(self, request):
        """
        Получение статистики по рассылкам.

        Информация по каждой рассылке дополняется полями
        delivered, sent и error, каждое из которых показывает
        количество сообщений по данной рассылке с определенным статусом
        """
        mailings = Mailing.objects.annotate(
            delivered=Count('messages', filter=Q(
                messages__status=Message.MessageStatus.DELIVERED
            )),
            sent=Count('messages', filter=Q(
                messages__status=Message.MessageStatus.SENT
            )),
            error=Count('messages', filter=Q(
                messages__status=Message.MessageStatus.ERROR
            ))
        )
        serializer = MailingStatisticSerializer(mailings, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    Эндпоинт для подробной информации по рассылкам.

    Позволяет получить информацию по сообщениям по любой рассылке
    """
    serializer_class = MessageSerializer

    def get_queryset(self):
        mailing_id = self.kwargs['mailing_id']
        mailing = get_object_or_404(Mailing, id=mailing_id)
        return mailing.messages.all()
