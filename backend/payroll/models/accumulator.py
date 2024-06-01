from uuid import uuid4

from django.db import models

from payroll.utils import AccumulatorUnits


class Accumulator(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    code = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    unit = models.CharField(
        max_length=20, choices=AccumulatorUnits.choices, default=AccumulatorUnits.AMOUNT
    )

    def __str__(self):
        return self.code
