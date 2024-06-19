from uuid import uuid4

from django.db import models

from payroll.utils import Units


class Accumulator(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    code = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=400)
    unit = models.CharField(max_length=20, choices=Units.choices, default=Units.AMOUNT)

    def __str__(self):
        return self.code

    def get_value(self, transactions):
        return sum(
            transactions.filter(
                allowance__type__type_accumulators__accumulator=self
            ).values_list(self.unit, flat=True)
        )
