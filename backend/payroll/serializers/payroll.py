from rest_framework import serializers

from payroll import models


class PayGroupSerializer(serializers.HyperlinkedModelSerializer):
    code = serializers.CharField()

    class Meta:
        model = models.PayGroup
        fields = ["url", "code", "description"]


class PayPeriodSerializer(serializers.HyperlinkedModelSerializer):
    group_code = serializers.CharField()

    class Meta:
        model = models.PayPeriod
        fields = [
            "url",
            "group_code",
            "frequency",
            "start",
            "end",
            "pay_date",
        ]
