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

    period_start = serializers.DateField()
    period_end = serializers.DateField()

    hours = serializers.FloatField()
    days = serializers.FloatField()
    weeks = serializers.FloatField()
    amount = serializers.FloatField()

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res["accumulators"] = [
            {
                "code": accumulator.code,
                "value": sum(
                    instance.transactions.filter(
                        allowance__type__type_accumulators__accumulator=accumulator,
                        for_period__start=res["period_start"],
                        for_period__end=res["period_end"],
                    ).values_list(f"{accumulator.unit}", flat=True)
                ),
                "unit": accumulator.unit,
            }
            for accumulator in models.Accumulator.objects.all()
        ]
        res["rates"] = [
            {
                "code": rate.code,
                "rate": rate.get_rate(instance, instance.period_start),
            }
            for rate in models.Rate.objects.all()
        ]
        return res

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
