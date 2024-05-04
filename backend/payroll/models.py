import uuid

from collections import defaultdict
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


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

    def clean(self):
        errors = defaultdict(list)

        try:
            self.first_name = self.first_name.title()
            self.middle_name = self.middle_name.title()
            self.last_name = self.last_name.title()
        except AttributeError:
            errors["name"].append("Name could not be parsed")

        tax_number = 0

        try:
            tax_number = int(self.tax_number)
        except ValueError:
            errors["tax_number"].append("Tax number must be a number")

        if not (10_000_000 < tax_number < 150_000_000):
            errors["tax_number"].append(
                "Tax numbers should be between 010-000-000 and 150-000-000"
            )

        # TODO check if tax number is valid

        if errors:
            raise serializers.ValidationError(errors)

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)


@receiver(pre_save, sender=Employee)
def employee_pre_save(sender, instance, **kwargs):
    # if not instance.tax_number:
    #     raise Exception("Tax number is required")

    instance.first_name = instance.first_name.title()
    instance.last_name = instance.last_name.title()
    instance.middle_name = instance.middle_name.title()


class SettingCategory(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100)
    order = models.IntegerField()

    def __str__(self):
        return self.name


class SettingCategoryField(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    category = models.ForeignKey(SettingCategory, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    order = models.IntegerField()

    def __str__(self):
        return self.name


class Setting(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    field = models.ForeignKey(SettingCategoryField, on_delete=models.CASCADE)

    effective_start = models.DateField()
    effective_end = models.DateField(null=True, blank=True)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """Model with UUID pk and contains payroll transactions"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    date = models.DateField()

    hours = models.FloatField()
    days = models.FloatField()
    weeks = models.FloatField()

    quantity = models.FloatField()
    rate = models.FloatField()
    factor = models.FloatField(default=1)
    amount = models.FloatField()
