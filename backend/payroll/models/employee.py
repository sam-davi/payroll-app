import uuid
from django.db import models
from datetime import datetime

from payroll.utils import FieldTypes
from payroll.models.tax import TaxCode


class EmployeeManager(models.Manager):
    def earnings_history(self):
        return self.annotate(
            period_end=models.F("transactions__for_period__end"),
            hours=models.Sum("transactions__hours"),
            days=models.Sum("transactions__days"),
            weeks=models.Sum("transactions__weeks"),
            amount=models.Sum("transactions__amount"),
        ).order_by("-period_end")


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

    objects = EmployeeManager()

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return " ".join([self.first_name, self.middle_name, self.last_name])

    @property
    def name(self):
        return " ".join([self.first_name, self.last_name])


class EmployeeCustomField(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField("Field Name", max_length=50)
    description = models.CharField("Field Description", max_length=200)

    type = models.CharField(
        "Field Type", choices=FieldTypes.choices, default=FieldTypes.STRING
    )


class EmployeeCustomFieldValue(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    field = models.ForeignKey(EmployeeCustomField, on_delete=models.CASCADE)
    _value = models.CharField("Value", max_length=200)

    effective_date = models.DateField(default=datetime.now)
