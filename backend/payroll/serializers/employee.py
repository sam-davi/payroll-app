from rest_framework import serializers

from payroll import models


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Employee
        fields = [
            "url",
            "user",
            "first_name",
            "middle_name",
            "last_name",
            "tax_number",
            "tax_code",
        ]


class EmployeeHistorySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    user = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    period_end = serializers.DateField()
    # accumulator = serializers.CharField()

    hours = serializers.FloatField()
    days = serializers.FloatField()
    weeks = serializers.FloatField()
    amount = serializers.FloatField()

    # class Meta:
    #     fields = [
    #         "url",
    #         "user",
    #         "first_name",
    #         "last_name",
    #         "period_end",
    #         "accumulator",
    #         "hours",
    #         "days",
    #         "weeks",
    #         "amount",
    #     ]
