from rest_framework import serializers
from mailing.models import (Client, Mailing, Message,
                            MailingFilter, FILTER_TYPE_CHOICES)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'phone_number', 'tag', 'timezone')


class MailingFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingFilter
        fields = ('filter_type', 'value')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('client', 'date_send', 'status')


class MailingSerializer(serializers.ModelSerializer):
    mailing_filters = MailingFilterSerializer(
        many=True,
        required=False,
        write_only=True
    )

    class Meta:
        model = Mailing
        fields = ('id', 'start_date', 'end_date', 'text', 'mailing_filters')

    def create_filters(self, instance, mailing_filters):
        filters_list = []
        for fil in mailing_filters:
            if fil['filter_type'] not in FILTER_TYPE_CHOICES:
                raise serializers.ValidationError('Несуществующий фильтр')
            filters_list.append(
                MailingFilter(
                    mailing=instance,
                    **fil
                )
            )
        MailingFilter.objects.bulk_create(filters_list)

    def create(self, validated_data):
        mailing_filters = validated_data.pop('mailing_filters')
        mailing = Mailing.objects.create(**validated_data)
        self.create_filters(mailing, mailing_filters)
        return mailing

    def update(self, instance, validated_data):
        mailing_filters = validated_data.pop('mailing_filters')
        instance.start_date = validated_data.get(
            'start_date',
            instance.start_date
        )
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.text = validated_data.get('text', instance.text)
        instance.mailing_filters.delete()
        self.create_filters(instance, mailing_filters)
        return instance
