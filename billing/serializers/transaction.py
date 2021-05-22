import datetime
from rest_framework import serializers
from billing.models import PaymentTransaction


class TransactionSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = PaymentTransaction
        exclude = ('user',)

    def get_date(self, obj):
        date_time_obj = datetime.datetime.strftime(obj.date, '%d.%m.%Y')
        return date_time_obj

