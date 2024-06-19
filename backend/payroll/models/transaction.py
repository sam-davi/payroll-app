from uuid import uuid4
from datetime import datetime, time, timedelta

from django.db import models

from .allowance import Allowance
from .employee import Employee
from .payroll import PayPeriod


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
    start = models.IntegerField(default=0)
    end = models.IntegerField(default=60 * 24 - 1)

    hours = models.FloatField()
    days = models.FloatField()
    weeks = models.FloatField()

    quantity = models.FloatField()
    rate = models.FloatField()
    factor = models.FloatField(default=1)
    amount = models.FloatField()

    @property
    def start_time(self):
        return datetime.combine(self.date, time()) + timedelta(minutes=self.start)

    @property
    def end_time(self):
        return datetime.combine(self.date, time()) + timedelta(minutes=self.end)

    @property
    def employee_code(self):
        return self.employee.code

    @employee_code.setter
    def employee_code(self, value):
        self.employee = Employee.objects.get(code=value)

    @property
    def allowance_code(self):
        return self.allowance.code

    @allowance_code.setter
    def allowance_code(self, value):
        self.allowance = Allowance.objects.get(code=value)

    @property
    def pay_period_code(self):
        return self.pay_period.code

    @pay_period_code.setter
    def pay_period_code(self, value):
        group_code, end = value.split()
        self.pay_period = PayPeriod.objects.get(group__code=group_code, end=end)

    @property
    def for_period_code(self):
        return self.for_period.code

    @for_period_code.setter
    def for_period_code(self, value):
        group_code, end = value.split()
        self.for_period = PayPeriod.objects.get(group__code=group_code, end=end)
