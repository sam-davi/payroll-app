from uuid import uuid4

from django.db import models

from payroll.models.allowance import Allowance
from payroll.models.employee import Employee
from payroll.models.payroll import PayPeriod


class Transaction(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

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
