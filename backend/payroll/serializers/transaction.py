from rest_framework import serializers

from payroll import models


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    employee_code = serializers.CharField()
    allowance_code = serializers.CharField()
    pay_period_code = serializers.CharField()
    for_period_code = serializers.CharField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    # rates = serializers.SerializerMethodField(read_only=True)

    # def get_rates(self, obj):
    #     rates = [
    #         {
    #             "code": rate.code,
    #             "numerator": (
    #                 numerator := rate.get_numerator(
    #                     employee=obj.employee, date=obj.for_period.start
    #                 )
    #             ),
    #             "denominator": (
    #                 denominator := rate.get_denominator(
    #                     employee=obj.employee, date=obj.for_period.start
    #                 )
    #             ),
    #             "factor": rate.factor,
    #             "rate": (
    #                 numerator * rate.factor / denominator if denominator != 0 else 0
    #             ),
    #             # "rate_detail": RateSerializer(rate, context=self.context).data,
    #         }
    #         for rate in models.Rate.objects.all()
    #     ]
    #     return rates

    class Meta:
        model = models.Transaction
        fields = [
            "url",
            "employee_code",
            "allowance_code",
            "pay_period_code",
            "for_period_code",
            # "date",
            # "start",
            # "end",
            "start_time",
            "end_time",
            "hours",
            "days",
            "weeks",
            "quantity",
            "rate",
            "factor",
            "amount",
            # "rates",
        ]
