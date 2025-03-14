from django.db import models

MIN_DATE = "1900-01-01"
MAX_DATE = "9999-12-31"


class Units(models.TextChoices):
    HOURS = "hours"
    DAYS = "days"
    WEEKS = "weeks"
    QUANTITY = "quantity"
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
