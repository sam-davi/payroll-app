# Generated by Django 5.0.3 on 2024-04-01 06:42

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0006_alter_employee_tax_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='SettingCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TaxCode',
            fields=[
                ('code', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='SettingCategoryField',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll.settingcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('effective_start', models.DateField()),
                ('effective_end', models.DateField(blank=True, null=True)),
                ('value', models.CharField(max_length=100)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll.employee')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll.settingcategoryfield')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='tax_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payroll.taxcode'),
        ),
    ]
