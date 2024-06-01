import uuid

from collections import defaultdict
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime, timedelta

class TaxCode(models.Model):
    code = models.CharField(primary_key=True, max_length=100)
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.code


class Employee(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, null=True, blank=True
    )

    first_name = models.CharField("First Name", max_length=100, null=True, blank=True)
    middle_name = models.CharField("Middle Name", max_length=100, null=True, blank=True)
    last_name = models.CharField("Last Name", max_length=100, null=True, blank=True)

    tax_number = models.CharField("Tax Number", max_length=100)
    tax_code = models.ForeignKey(
        TaxCode, verbose_name="Tax Code", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return " ".join([self.first_name, self.middle_name, self.last_name])

    @property
    def name(self):
        return " ".join([self.first_name, self.last_name])


class PayGroup(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    code = models.CharField(max_length=100)
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.code


class PayFreqeuncy(models.TextChoices):
    WEEKLY = "weekly"
    FORTNIGHTLY = "fortnightly"
    FOURWEEKLY = "fourweekly"
    MONTHLY = "monthly"


class PayPeriod(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    group = models.ForeignKey(PayGroup, on_delete=models.CASCADE)

    frequency = models.CharField(
        max_length=20, choices=PayFreqeuncy.choices, default=PayFreqeuncy.WEEKLY
    )

    start = models.DateField()
    end = models.DateField()
    pay_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.group} - {self.end}"


class AllowanceType(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    code = models.CharField(max_length=100)
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.code


class AccumulatorUnits(models.TextChoices):
    HOURS = "hours"
    DAYS = "days"
    WEEKS = "weeks"
    AMOUNT = "amount"


class Accumulator(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    code = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    unit = models.CharField(
        max_length=20, choices=AccumulatorUnits.choices, default=AccumulatorUnits.AMOUNT
    )

    def __str__(self):
        return self.code


class AllowanceTypeAccumulator(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    type = models.ForeignKey(
        AllowanceType, related_name="type_accumulators", on_delete=models.CASCADE
    )
    accumulator = models.ForeignKey(
        Accumulator, related_name="allowance_types", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.accumulator} - {self.type}"


class Allowance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    code = models.CharField(max_length=100)
    description = models.CharField(max_length=400)

    type = models.ForeignKey(
        AllowanceType, related_name="allowances", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.code


class Transaction(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    employee = models.ForeignKey(
        Employee, related_name="transactions", on_delete=models.CASCADE, null=True
    )
    allowance = models.ForeignKey(
        Allowance, related_name="transactions", on_delete=models.CASCADE, null=True
    )

    pay_period = models.ForeignKey(
        PayPeriod,
        related_name="pay_period_transactions",
        on_delete=models.CASCADE,
        null=True,
    )
    for_period = models.ForeignKey(
        PayPeriod,
        related_name="for_period_transactions",
        on_delete=models.CASCADE,
        null=True,
    )

    date = models.DateField()

    hours = models.FloatField()
    days = models.FloatField()
    weeks = models.FloatField()

    quantity = models.FloatField()
    rate = models.FloatField()
    factor = models.FloatField(default=1)
    amount = models.FloatField()


class ReferenceDates(models.TextChoices):
    PERIOD_DATE = "period_date"
    TRANSACTION_DATE = "transaction_date"


class Rate(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

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
