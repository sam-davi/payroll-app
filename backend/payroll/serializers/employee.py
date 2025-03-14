from rest_framework import serializers

from payroll import models


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Employee
        fields = [
            "url",
            "code",
            "first_name",
            "middle_name",
            "last_name",
            "tax_number",
            "tax_code",
        ]


class EmployeeHistorySerializer(serializers.Serializer):
    id = serializers.UUIDField()

    code = serializers.CharField()
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
        transactions = instance.transactions.filter(
            for_period__start=res["period_start"],
            for_period__end=res["period_end"],
        )
        if transactions.count() == 0:
            return res
        res["accumulators"] = [
            {
                "code": accumulator.code,
                "value": accumulator.get_value(transactions),
                "unit": accumulator.unit,
            }
            for accumulator in models.Accumulator.objects.all().order_by("code")
        ]
        res["rates"] = [
            {
                "code": rate.code,
                "rate": rate.get_rate(instance, instance.period_start),
                "unit": rate.unit,
            }
            for rate in models.Rate.objects.all().order_by("code")
        ]
        return res


class EmployeeCustomFieldSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.EmployeeCustomField
        fields = ["url", "name", "description", "type"]


class EmployeeCustomFieldValueSerializer(serializers.HyperlinkedModelSerializer):
    employee_code = serializers.CharField()
    field_name = serializers.CharField()
    field_code = serializers.ReadOnlyField(source="field.code")
    field_value = serializers.CharField()

    class Meta:
        model = models.EmployeeCustomFieldValue
        fields = [
            "url",
            "employee_code",
            "field_name",
            "field_code",
            "field_value",
            "effective_date",
        ]
