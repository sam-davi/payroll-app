from django.db import models


class AccumulatorUnits(models.TextChoices):
    HOURS = "hours"
    DAYS = "days"
    WEEKS = "weeks"
    AMOUNT = "amount"


class FieldTypes(models.TextChoices):
    STRING = "str"
    INTEGER = "int"
    FLOAT = "float"
    DATE = "date"


class PayFrequency(models.TextChoices):
    WEEKLY = "weekly"
    FORTNIGHTLY = "fortnightly"
    FOURWEEKLY = "fourweekly"
    MONTHLY = "monthly"


class ReferenceDates(models.TextChoices):
    PERIOD_DATE = "period_date"
    TRANSACTION_DATE = "transaction_date"
