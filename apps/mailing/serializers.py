from rest_framework import serializers

from apps.mailing.models import Mailing, MailingFilter, Message


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
            if fil['filter_type'] not in MailingFilter.MailingFilterChoices:
                raise serializers.ValidationError('Несуществующий фильтр')
            filters_list.append(
                MailingFilter(
                    mailing=instance,
                    **fil
                )
            )
        MailingFilter.objects.bulk_create(filters_list)

    def create(self, validated_data):
        mailing_filters = validated_data.get('mailing_filters', [])
        mailing = Mailing.objects.create(
            status=Mailing.MailingStatus.WAITING,
            **validated_data
        )
        self.create_filters(mailing, mailing_filters)

        # Здесь должен быть таск на запуск этой рассылки
        # В зависимости от start_date И end_date

        return mailing

    def update(self, instance, validated_data):
        mailing_filters = validated_data.get('mailing_filters', [])

        instance.start_date = validated_data.get(
            'start_date',
            instance.start_date
        )
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.text = validated_data.get('text', instance.text)
        instance.mailing_filters.delete()
        self.create_filters(instance, mailing_filters)
        return instance


class MailingStatisticSerializer(MailingSerializer):
    delivered = serializers.IntegerField()
    sent = serializers.IntegerField()
    error = serializers.IntegerField()

    class Meta:
        model = Mailing
        fields = ('id', 'start_date', 'end_date',
                  'text', 'mailing_filters', 'delivered', 'sent', 'error')
