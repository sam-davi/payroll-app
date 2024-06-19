from uuid import uuid4

from django.db import models
from django.utils.text import slugify

from payroll.utils import PayFrequency


class PayGroup(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    code = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.code

    @property
    def group_code(self):
        return self.code

    @group_code.setter
    def group_code(self, value):
        self.code = slugify(value)


class PayPeriod(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    group = models.ForeignKey(PayGroup, on_delete=models.CASCADE)

    frequency = models.CharField(
        max_length=20, choices=PayFrequency.choices, default=PayFrequency.WEEKLY
    )

    start = models.DateField()
    end = models.DateField()
    pay_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ["group", "end"]

    def __str__(self):
        return f"{self.group.code} {self.end}"

    @property
    def group_code(self):
        return self.group.code

    @group_code.setter
    def group_code(self, value):
        self.group = PayGroup.objects.get(code=slugify(value))

    @property
    def code(self):
        return f"{self.group.code} {self.end}"
