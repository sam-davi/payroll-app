from uuid import uuid4
from datetime import timedelta

from django.db import models

from payroll.utils import Units, ReferenceDates
from .accumulator import Accumulator
from .transaction import Transaction


class Rate(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    code = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=400)

    unit = models.CharField(max_length=20, choices=Units.choices, default=Units.HOURS)

    numerator = models.ForeignKey(
        Accumulator, related_name="as_numerator_rates", on_delete=models.CASCADE
    )
    denominator = models.ForeignKey(
        Accumulator, related_name="as_denominator_rates", on_delete=models.CASCADE
    )

    denominator_cap = models.FloatField(default=9999999)

    factor = models.FloatField(default=1)

    days_range = models.IntegerField(default=1)

    reference_date = models.CharField(
        max_length=100,
        choices=ReferenceDates.choices,
        default=ReferenceDates.TRANSACTION_DATE,
    )

    def __str__(self):
        return self.code

    @property
    def numerator_code(self):
        return self.numerator.code

    @numerator_code.setter
    def numerator_code(self, value):
        self.numerator = Accumulator.objects.get(code=value)

    @property
    def denominator_code(self):
        return self.denominator.code

    @denominator_code.setter
    def denominator_code(self, value):
        self.denominator = Accumulator.objects.get(code=value)

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
        transactions = self.get_range(employee, date)
        return self.numerator.get_value(transactions)

    def get_denominator(self, employee, date):
        transactions = self.get_range(employee, date)
        return min(self.denominator_cap, self.denominator.get_value(transactions))

    def get_rate(self, employee, date):
        denominator = self.get_denominator(employee, date)
        return (
            0
            if denominator == 0
            else self.get_numerator(employee, date) * self.factor / denominator
        )
