from uuid import uuid4

from django.db import models

from .accumulator import Accumulator


class AllowanceType(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    code = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.code


class AllowanceTypeAccumulator(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    type = models.ForeignKey(
        AllowanceType, related_name="type_accumulators", on_delete=models.CASCADE
    )
    accumulator = models.ForeignKey(
        Accumulator, related_name="allowance_types", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (("type", "accumulator"),)

    def __str__(self):
        return f"{self.accumulator} - {self.type}"

    @property
    def type_code(self):
        return self.type.code

    @type_code.setter
    def type_code(self, value):
        self.type = AllowanceType.objects.get(code=value)

    @property
    def accumulator_code(self):
        return self.accumulator.code

    @accumulator_code.setter
    def accumulator_code(self, value):
        self.accumulator = Accumulator.objects.get(code=value)


class Allowance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    code = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=400)

    type = models.ForeignKey(
        AllowanceType, related_name="allowances", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.code

    @property
    def type_code(self):
        return self.type.code

    @type_code.setter
    def type_code(self, value):
        self.type = AllowanceType.objects.get(code=value)
