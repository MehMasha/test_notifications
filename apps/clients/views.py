
from rest_framework import viewsets

from apps.clients.models import Client
from apps.clients.serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """
    Эндпоинты для работы с клиентами.

    Добавление новых клиентов, изменение клиентов и их удаление
    """
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
