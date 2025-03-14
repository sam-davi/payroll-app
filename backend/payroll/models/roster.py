from uuid import uuid4
import datetime

from django.db import models

from payroll.utils import MIN_DATE, MAX_DATE

from .employee import Employee


class Roster(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    code = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=400)

    cycle_length = models.IntegerField(default=7)

    def __str__(self):
        return self.code


class Shift(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    code = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=400)

    start = models.IntegerField(default=8.5 * 60)
    end = models.IntegerField(default=17 * 60)

    unpaid_break = models.IntegerField(default=30)

    def __str__(self):
        return self.code

    @property
    def start_time(self):
        return datetime.time(hour=self.start // 60 % 24, minute=self.start % 60)

    @property
    def end_time(self):
        return datetime.time(hour=self.end // 60 % 24, minute=self.end % 60)

    @property
    def crosses_midnight(self):
        return self.end >= 24 * 60 and self.start < 24 * 60

    @property
    def hours(self):
        return (self.end - self.start - self.unpaid_break) / 60


class RosterShift(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    roster = models.ForeignKey(
        Roster, related_name="shifts", on_delete=models.CASCADE, null=True
    )

    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, null=True)

    order = models.IntegerField(default=0)

    def __str__(self):
        return self.code

    @property
    def roster_code(self):
        return self.roster.code

    @roster_code.setter
    def roster_code(self, value):
        self.roster = Roster.objects.get(code=value)

    @property
    def shift_code(self):
        return self.shift.code

    @shift_code.setter
    def shift_code(self, value):
        self.shift = Shift.objects.get(code=value)

    @property
    def day(self):
        return self.order + 1

    @day.setter
    def day(self, value: int):
        if value < 1 or value > self.roster.cycle_length:
            raise ValueError
        self.order = value - 1

    @property
    def start(self):
        return self.shift.start

    @property
    def end(self):
        return self.shift.end

    @property
    def unpaid_break(self):
        return self.shift.unpaid_break

    @property
    def hours(self):
        return self.shift.hours

    @property
    def start_time(self):
        return self.shift.start_time

    @property
    def end_time(self):
        return self.shift.end_time


class RosterEmployee(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    roster = models.ForeignKey(
        Roster, related_name="employees", on_delete=models.CASCADE, null=True
    )

    employee = models.ForeignKey(
        "payroll.Employee", related_name="roster_employees", on_delete=models.CASCADE
    )

    effective_start = models.DateField(default=MIN_DATE)
    effective_end = models.DateField(default=MAX_DATE)

    offset = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.roster.code} - {self.employee}"

    @property
    def roster_code(self):
        return self.roster.code

    @roster_code.setter
    def roster_code(self, value):
        self.roster = Roster.objects.get(code=value)

    @property
    def employee_code(self):
        return self.employee.code

    @employee_code.setter
    def employee_code(self, value):
        self.employee = Employee.objects.get(code=value)

    def get_shift(self, date: datetime.date):
        try:
            if self.effective_start > date or date > self.effective_end:
                return []
        except TypeError:
            return []
        order = (
            date - self.effective_start - datetime.timedelta(days=self.offset)
        ).days % self.roster.cycle_length
        return self.roster.shifts.filter(order=order)

    def get_shifts(self, dates=None):
        if dates is None:
            dates = [
                self.effective_start + datetime.timedelta(days=day)
                for day in range(self.roster.cycle_length)
            ]

        return [
            {
                "date": date,
                "shift": shift.shift_code,
                "start": shift.start,
                "end": shift.end,
                "start_time": shift.start_time,
                "end_time": shift.end_time,
                "hours": shift.hours,
            }
            for date in dates
            for shift in self.get_shift(date)
            if shift is not None
        ]
