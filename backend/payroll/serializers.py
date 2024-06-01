from rest_framework import serializers
from payroll import models

from django.db.models import F


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


class TaxCodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.TaxCode
        fields = ["url", "code", "description"]


class AllowanceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.AllowanceType
        fields = ["url", "code", "description"]


class AllowanceSerializer(serializers.HyperlinkedModelSerializer):
    type_detail = AllowanceTypeSerializer(source="type", read_only=True)

    class Meta:
        model = models.Allowance
        fields = ["url", "code", "description", "type", "type_detail"]


class AccumulatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Accumulator
        fields = ["url", "code", "description", "unit"]


class AllowanceTypeAccumulatorSerializer(serializers.HyperlinkedModelSerializer):
    type_detail = AllowanceTypeSerializer(source="type", read_only=True)
    accumulator_detail = AccumulatorSerializer(source="accumulator", read_only=True)

    class Meta:
        model = models.AllowanceTypeAccumulator
        fields = ["url", "type", "type_detail", "accumulator", "accumulator_detail"]


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    employee_detail = EmployeeSerializer(source="employee", read_only=True)
    allowance_detail = AllowanceSerializer(source="allowance", read_only=True)
    pay_period_detail = PayPeriodSerializer(source="pay_period", read_only=True)
    for_period_detail = PayPeriodSerializer(source="for_period", read_only=True)
    rates = serializers.SerializerMethodField(read_only=True)

    def get_rates(self, obj):
        rates = [
            {
                "code": rate.code,
                "numerator": (
                    numerator := rate.get_numerator(
                        employee=obj.employee, date=obj.for_period.start
                    )
                ),
                "denominator": (
                    denominator := rate.get_denominator(
                        employee=obj.employee, date=obj.for_period.start
                    )
                ),
                "factor": rate.factor,
                "rate": (
                    numerator * rate.factor / denominator if denominator != 0 else 0
                ),
                "rate_detail": RateSerializer(rate, context=self.context).data,
            }
            for rate in models.Rate.objects.all()
        ]
        return rates

    class Meta:
        model = models.Transaction
        fields = [
            "url",
            "employee",
            "employee_detail",
            "allowance",
            "allowance_detail",
            "pay_period",
            "pay_period_detail",
            "for_period",
            "for_period_detail",
            "date",
            "hours",
            "days",
            "weeks",
            "quantity",
            "rate",
            "factor",
            "amount",
            "rates",
        ]


# class AccumulatorValueSerializer(serializers.HyperlinkedModelSerializer):
#     value = serializers.FloatField(read_only=True)

#     def to_representation(self, instance):
#         results = super().to_representation(instance)
#         values = instance.allowance_types.filter(
#             type__allowances__transactions__isnull=False
#         ).values(
#             employee=F("type__allowances__transactions__employee"),
#             date=F("type__allowances__transactions__date"),
#             value=F(f"type__allowances__transactions__{instance.unit}"),
#         )
#         results["value"] = values
#         return results

#     class Meta:
#         model = models.Accumulator
#         fields = ["url", "code", "description", "unit", "value"]


# class TransactionAccumulatorSerializer(serializers.HyperlinkedModelSerializer):
#     employee_detail = EmployeeSerializer(source="employee", read_only=True)
#     values = serializers.SerializerMethodField(read_only=True)

#     def get_values(self, instance):
#         values = AccumulatorSerializer(
#             [x.accumulator for x in instance.allowance.type.type_accumulators.all()],
#             many=True,
#             context=self.context,
#         ).data
#         for value in values:
#             value["value"] = getattr(instance, value["unit"])
#         return values

#     class Meta:
#         model = models.Transaction
#         fields = ["url", "employee", "employee_detail", "date", "values"]


class RateSerializer(serializers.HyperlinkedModelSerializer):
    numerator_detail = AccumulatorSerializer(source="numerator", read_only=True)
    denominator_detail = AccumulatorSerializer(source="denominator", read_only=True)

    class Meta:
        model = models.Rate
        fields = [
            "url",
            "code",
            "description",
            "numerator",
            "numerator_detail",
            "denominator",
            "denominator_detail",
            "factor",
            "days_range",
            "reference_date",
        ]
