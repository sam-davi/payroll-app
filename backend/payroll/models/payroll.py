from uuid import uuid4

from django.db import models

from payroll.utils import PayFrequency


class PayGroup(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    code = models.CharField(max_length=100)
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.code


class PayPeriod(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    group = models.ForeignKey(PayGroup, on_delete=models.CASCADE)

    frequency = models.CharField(
        max_length=20, choices=PayFrequency.choices, default=PayFrequency.WEEKLY
    )

    start = models.DateField()
    end = models.DateField()
    pay_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.group} - {self.end}"
