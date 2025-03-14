from datetime import datetime, date
from uuid import uuid4

from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from payroll.utils import FieldTypes, MIN_DATE
from .tax import TaxCode


def generate_code():
    return get_random_string(5, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")


class EmployeeManager(models.Manager):
    def earnings_history(self):
        return self.annotate(
            period_start=models.F("transactions__for_period__start"),
            period_end=models.F("transactions__for_period__end"),
            hours=models.Sum("transactions__hours"),
            days=models.Sum("transactions__days"),
            weeks=models.Sum("transactions__weeks"),
            amount=models.Sum("transactions__amount"),
        ).order_by("period_start")


class Employee(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    code = models.CharField(
        "Employee Code", max_length=5, default=generate_code, unique=True
    )

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

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    name = models.CharField("Field Name", max_length=50)
    code = models.CharField("Field Code", max_length=50, unique=True)
    description = models.CharField("Field Description", max_length=200)

    type = models.CharField(
        "Field Type", choices=FieldTypes.choices, default=FieldTypes.STRING
    )

    def save(self, *args, **kwargs):
        self.code = slugify(self.name)
        return super(EmployeeCustomField, self).save(*args, **kwargs)


class EmployeeCustomFieldValue(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    field = models.ForeignKey(EmployeeCustomField, on_delete=models.CASCADE)
    value = models.CharField("Value", max_length=200, null=True)

    effective_date = models.DateField(default=MIN_DATE)

    @property
    def field_value(self):
        if self.field.type == FieldTypes.STRING:
            return self.value
        if self.field.type == FieldTypes.INTEGER:
            return int(self.value)
        if self.field.type == FieldTypes.FLOAT:
            return float(self.value)
        if self.field.type == FieldTypes.DATE:
            return date.fromisoformat(self.value)
        return self.value

    @field_value.setter
    def field_value(self, value):
        if value is None:
            self.value = None
        self.value = str(value)

    @property
    def field_name(self):
        return self.field.name

    @field_name.setter
    def field_name(self, value):
        self.field = EmployeeCustomField.objects.get(code=slugify(value))

    @property
    def employee_code(self):
        return self.employee.code

    @employee_code.setter
    def employee_code(self, value):
        self.employee = Employee.objects.get(code=value)
