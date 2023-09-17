from rest_framework import serializers

from apps.clients.models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'phone_number', 'tag', 'timezone')
