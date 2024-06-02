from rest_framework import serializers

from payroll import models


class PayGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.PayGroup
        fields = ["url", "code", "description"]


class PayPeriodSerializer(serializers.HyperlinkedModelSerializer):
    group_detail = PayGroupSerializer(source="group", read_only=True)

    class Meta:
        model = models.PayPeriod
        fields = [
            "url",
            "group",
            "group_detail",
            "frequency",
            "start",
            "end",
            "pay_date",
        ]
