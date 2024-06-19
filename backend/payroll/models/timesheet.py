from uuid import uuid4
from datetime import datetime, time, timedelta

from django.db import models

from .employee import Employee


class Timesheet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    employee = models.ForeignKey(
        "payroll.Employee", related_name="timesheets", on_delete=models.CASCADE
    )

    date = models.DateField()

    start = models.IntegerField()
    end = models.IntegerField()

    unpaid_break = models.IntegerField(default=30)

    @property
    def employee_code(self):
        return self.employee.code

    @employee_code.setter
    def employee_code(self, value):
        self.employee = Employee.objects.get(code=value)

    @property
    def start_time(self):
        return datetime.combine(self.date, time()) + timedelta(minutes=self.start)

    @property
    def end_time(self):
        return datetime.combine(self.date, time()) + timedelta(minutes=self.end)

    @property
    def hours(self):
        return (self.end - self.start - self.unpaid_break) / 60
