from rest_framework import serializers

from payroll import models
from .employee import EmployeeSerializer
from .allowance import AllowanceSerializer
from .payroll import PayPeriodSerializer
from .rate import RateSerializer


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
