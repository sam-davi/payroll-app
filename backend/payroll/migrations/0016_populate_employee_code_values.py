# Generated by Django 5.0.3 on 2024-06-12 03:53

from payroll.models.employee import generate_code
from django.db import migrations


def gen_code(apps, schema_editor):
    Employee = apps.get_model("payroll", "Employee")
    for employee in Employee.objects.all():
        employee.code = generate_code()
        employee.save(update_fields=["code"])


class Migration(migrations.Migration):

    dependencies = [
        ("payroll", "0015_add_employee_code_field"),
    ]

    operations = [
        migrations.RunPython(gen_code),
    ]
