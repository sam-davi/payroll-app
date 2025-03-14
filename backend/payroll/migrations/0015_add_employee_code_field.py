# Generated by Django 5.0.3 on 2024-06-12 03:52

import payroll.models.employee
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payroll", "0014_transaction_end_transaction_start"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="code",
            field=models.CharField(
                default=payroll.models.employee.generate_code,
                max_length=5,
                null=True,
                verbose_name="Employee Code",
            ),
        ),
    ]
