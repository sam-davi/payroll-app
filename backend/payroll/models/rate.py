from uuid import uuid4
from datetime import timedelta

from django.db import models

from payroll.models.accumulator import Accumulator
from payroll.models.transaction import Transaction
from payroll.utils import ReferenceDates


class Rate(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    code = models.CharField(max_length=100)
    description = models.CharField(max_length=400)

    numerator = models.ForeignKey(
        Accumulator, related_name="as_numerator_rates", on_delete=models.CASCADE
    )
    denominator = models.ForeignKey(
        Accumulator, related_name="as_denominator_rates", on_delete=models.CASCADE
    )

    factor = models.FloatField(default=1)

    days_range = models.IntegerField(default=1)

    reference_date = models.CharField(
        max_length=100,
        choices=ReferenceDates.choices,
        default=ReferenceDates.TRANSACTION_DATE,
    )

    def __str__(self):
        return self.code

    def get_range(self, employee, date):
        transactions = Transaction.objects.filter(employee=employee)
        from_date = date - timedelta(days=self.days_range)
        if self.reference_date == ReferenceDates.TRANSACTION_DATE:
            transactions = transactions.filter(date__lt=date, date__gte=from_date)
        if self.reference_date == ReferenceDates.PERIOD_DATE:
            transactions = transactions.filter(
                for_period__end__lt=date, for_period__end__gte=from_date
            )
        return transactions

    def get_numerator(self, employee, date):
        return sum(
            self.get_range(employee, date)
            .filter(allowance__type__type_accumulators__accumulator=self.numerator)
            .values_list(f"{self.numerator.unit}", flat=True)
        )

    def get_denominator(self, employee, date):
        return sum(
            self.get_range(employee, date)
            .filter(allowance__type__type_accumulators__accumulator=self.denominator)
            .values_list(f"{self.denominator.unit}", flat=True)
        )

    def get_rate(self, employee, date):
        denominator = self.get_denominator(employee, date)
        return (
            0
            if denominator == 0
            else self.get_numerator(employee, date) * self.factor / denominator
        )
