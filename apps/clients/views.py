
from rest_framework import viewsets
import logging

from apps.clients.models import Client
from apps.clients.serializers import ClientSerializer


logger = logging.getLogger('json_logger')


class ClientViewSet(viewsets.ModelViewSet):
    """
    Эндпоинты для работы с клиентами.

    Добавление новых клиентов, изменение клиентов и их удаление
    """
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def list(self, request, *args, **kwargs):
        logger.info("Get list of clients")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info(
            "detail of client",
            extra={
                "client_id": kwargs.get('pk')
            }
        )
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        if 'csrfmiddlewaretoken' in data:
            del data['csrfmiddlewaretoken']
        logger.info(
            'Creating a new client',
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
            'Updating a client',
            extra={
                "client_id": kwargs["pk"],
                "data": request.data
            }
        )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.info(
            'Deleting a client',
            extra={
                "client_id": kwargs["pk"]
            }
        )
        return super().destroy(request, *args, **kwargs)
