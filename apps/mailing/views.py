import logging

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.mailing.models import Mailing, Message
from apps.mailing.serializers import (MailingSerializer,
                                      MailingStatisticSerializer,
                                      MessageSerializer)

logger = logging.getLogger('json_logger')


class MailingViewSet(viewsets.ModelViewSet):
    """
    Эндпоинты для информации по рассылкам.

    Позволяют получить информацию по одному или нескольким рассылкам,
    изменять их или удалять
    """
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()

    def list(self, request, *args, **kwargs):
        logger.info("Get list of mailings")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info(
            "detail of mailings",
            extra={
                "mailing_id": kwargs.get('pk')
            }
        )
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        if 'csrfmiddlewaretoken' in data:
            del data['csrfmiddlewaretoken']
        logger.info(
            'Creating a new mailing',
            extra={
                "data": request.data
            }
        )
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        data = dict(request.data)
        if 'csrfmiddlewaretoken' in data:
            del data['csrfmiddlewaretoken']
        logger.info(
            'Updating a mailing',
            extra={
                "mailing_id": kwargs["pk"],
                "data": request.data
            }
        )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.info(
            'Deleting a mailing',
            extra={
                "mailing_id": kwargs["pk"]
            }
        )
        return super().destroy(request, *args, **kwargs)

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
        logger.info("Get mailings statistic")
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

    def list(self, request, *args, **kwargs):
        logger.info(
            "Get list of mailings messages",
            extra={
                "mailing_id": kwargs.get("mailing_id")
            }
        )
        return super().list(request, *args, **kwargs)
